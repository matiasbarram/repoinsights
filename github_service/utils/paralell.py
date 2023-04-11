from concurrent.futures import ThreadPoolExecutor, as_completed


def run_in_parallel(function, args_list, max_workers=5):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Envía las tareas al ThreadPoolExecutor
        futures = [executor.submit(function, *args) for args in args_list]

        # Espera a que se completen todas las tareas y recupera sus resultados
        for future in as_completed(futures):
            results.append(future.result())

    return results
