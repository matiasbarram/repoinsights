from dotenv import load_dotenv
import DWConnector.main as DWService

load_dotenv()

dw_connector = DWService.DWConnector()
repos = dw_connector.get_repos()
