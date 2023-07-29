#!/bin/bash

dir=$1

if [ -z "$dir" ]; then
    echo "Uso: $0 <ruta/del/archivo.log>"
    exit 1
fi

function get_repo_name {
    log_file=$1
    echo $log_file
}

function log_time {
    log_file=$1
    start_time=$(cat "$log_file" | grep "Extracting from GitHub" | awk '{print $1, $2}' | head -n 1)
    end_time=$(cat "$log_file" | grep "Project ENQUEUE to CURADO published" | awk '{print $1, $2}' | tail -n 1)
    
    if [ -n "$start_time" ] && [ -n "$end_time" ]; then
        start_epoch=$(date -d "$start_time" +%s)
        end_epoch=$(date -d "$end_time" +%s)

        total_time=$((end_epoch - start_epoch))
        echo $total_time
    fi
}

function api_calls {
    log_file=$1
    api_calls=$(grep ".| DEBUG    | services.extract_service.extract_module.github_api.github_api" $log_file | wc -l)
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
    total_calls=$(api_calls $file)
    result+=$sep$(create_json "$repo_name" $total_time $total_calls)
    sep=', '
done
result+=']'

echo $result > extract_results.json
