from services.generate_metrics.calculate_metrics import InsightsMetrics
from pprint import pprint


def main(project_id):
    metrics = InsightsMetrics(project_id)
    results = metrics.calculate_metrics()
    metrics.load_metrics(results)


if __name__ == "__main__":
    main(10380)
    main(1)
