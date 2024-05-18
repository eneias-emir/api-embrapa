import json
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from api_embrapa.application import _create_app
from api_embrapa.model_resp_api import RespApiImportacaoExportacao, RespApi

app = _create_app()

client = TestClient(app)

user_name = "test_user"
password  = "test_password"
test_user = {
  "username": user_name,
  "password": password
}
txt_content_test_user = f"username={user_name}&password={password}"
txt_content_test_invalid_user = "username=invalid_user&password=invalid_pwd"

def get_endpoints_data(endpoint: str):
    response = client.post("/api/v1/token", content=txt_content_test_user, headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    token = response.json() 
    access_token = token["access_token"]
    response = client.get(f"/api/v1/inventory/{endpoint}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

def get_endpoints_data_filter(endpoint: str):
    response = client.post("/api/v1/token", content=txt_content_test_user, headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    token = response.json() 
    access_token = token["access_token"]
    response = client.get(f"/api/v1/inventory/{endpoint}/2022", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200

    adapter = TypeAdapter(list[RespApi])
    items = adapter.validate_python(response.json())

    assert items[0].atividade != ''
    assert items[0].tipo != ''
    assert items[0].produto != ''
    assert items[0].itens != []
    assert items[0].itens[0].ano != ''


def get_endpoints_data_filter_import_export(endpoint: str):
    response = client.post("/api/v1/token", content=txt_content_test_user, headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    token = response.json() 
    access_token = token["access_token"]
    response = client.get(f"/api/v1/inventory/{endpoint}/2022", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200

    adapter = TypeAdapter(list[RespApiImportacaoExportacao])
    items = adapter.validate_python(response.json())

    assert items[0].atividade != ''
    assert items[0].tipo != ''
    assert items[0].pais != ''
    assert items[0].itens != []
    assert items[0].itens[0].ano != ''


def test_read_root():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

def test_read_base_url():
    response = client.get("/api/v1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}   

def test_read_base_url_inventory():
    response = client.get("/api/v1/inventory/")
    assert response.status_code == 200
    assert response.json() == {'name': 'API Embrapa', 'description': 'Banco de dados de uva, vinho e derivados - Embrapa Uva e Vinho', 'endpoints': ['http://testserver/api/v1/inventory/production', 'http://testserver/api/v1/inventory/processing', 'http://testserver/api/v1/inventory/comercialization', 'http://testserver/api/v1/inventory/imports', 'http://testserver/api/v1/inventory/exports', 'http://testserver/api/v1/inventory/all']}

def test_read_base_url_inventory_production():
    response = client.get("/api/v1/inventory/production")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_read_base_url_inventory_comercialization():
    response = client.get("/api/v1/inventory/comercialization")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_register():
    response = client.post("/api/v1/login/register", content=json.dumps(test_user))
    assert response.status_code == 201
    assert response.json() == {'user': 'test_user', 'status': 'Registred successfully'}

def test_get_token():
    response = client.post("/api/v1/token", content=txt_content_test_user, headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.status_code == 200

def test_get_token_invalid_user():
    response = client.post("/api/v1/token", content=txt_content_test_invalid_user, headers={ 'Content-Type': 'application/x-www-form-urlencoded'})
    assert response.status_code == 401

def test_endpoints_data():
    get_endpoints_data("production")
    get_endpoints_data("processing")
    get_endpoints_data("comercialization")
    get_endpoints_data("imports")
    get_endpoints_data("exports")

def test_endpoints_data_filter():
    get_endpoints_data_filter('production')
    get_endpoints_data_filter('processing')
    get_endpoints_data_filter('comercialization')

def test_endpoints_data_filter_import_export():
    get_endpoints_data_filter_import_export('imports')
    get_endpoints_data_filter_import_export('exports')


