#!/bin/bash

dir=$1

if [ -z "$dir" ]; then
    echo "Usage: $0 <path/to/log/file>"
    exit 1
fi

function get_repo_name {
    log_file=$1
    echo $log_file
}

function log_time {
    log_file=$1
    start_time=$(cat "$log_file" | grep "Extracting from GitHub" | grep "DESDE -> None" | awk '{print $1, $2}' | head -n 1)
    end_time=$(cat "$log_file" | grep "Project ENQUEUE to CURADO published" | awk '{print $1, $2}' | tail -n 1)
    
    if [ -z "$start_time" ] || [ -z "$end_time" ]; then
        echo "-1"
        return
    fi

    start_epoch=$(date -d "$start_time" +%s)
    end_epoch=$(date -d "$end_time" +%s)

    total_time=$((end_epoch - start_epoch))
    echo $total_time
}

function api_calls {
    log_file=$1
    api_calls=$(grep "services.extract_service.extract_module.github_api.github_api:get" $log_file | wc -l)
    if [ -z "$api_calls" ]; then
        echo "-1"
        return
    fi
    echo $api_calls
}

function create_json {
    repo_name=$1
    total_time=$2
    total_calls=$3
    json_string='{"repo": "'$repo_name'", "time": '$total_time', "calls": '$total_calls'}'
    echo $json_string
}

result='['
sep=''
for file in $(find $dir -name "*.log" -path "*extract*"); do
    repo_name=$(get_repo_name $file)
    total_time=$(log_time $file)
    if [ "$total_time" -eq "-1" ]; then
        echo "Start or End time not found in $repo_name"
        continue
    fi
    total_calls=$(api_calls $file)
    if [ "$total_calls" -eq "-1" ]; then
        echo "No API calls found in $repo_name"
        continue
    fi
    result+=$sep$(create_json "$repo_name" $total_time $total_calls)
    sep=', '
done
result+=']'

echo $result > extract_results.json

