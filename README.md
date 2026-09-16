# Business Procurement Agent - Prototype tối giản

Project này minh họa luồng cơ bản nhất của một ứng dụng Python gửi prompt tới
Hermes Agent API Server và in phản hồi ra terminal.

Project dùng package `openai` như một OpenAI-compatible client. Code không gọi
OpenAI trực tiếp và không phụ thuộc vào StepFun hay một model cụ thể. Prototype
chưa sử dụng FastAPI, database, frontend, tool calling hoặc agent framework khác.

## Chạy lại sau khi đã cấu hình

Mở PowerShell thứ nhất và giữ gateway chạy:

```powershell
hermes gateway run
```

Nếu gateway đã chạy ở nền và `/health` trả `ok`, không cần mở thêm gateway.
Trong PowerShell thứ hai, tại thư mục project:

```powershell
python main.py
```

Lệnh `hermes` mở chat trong terminal; project Python cần API server được bật
và gateway đang chạy. Các bước bên dưới chỉ cần thực hiện khi cài/cấu hình lần đầu.

## Cấu trúc project

```text
.
|-- .env              # Chứa API key trên máy cá nhân, không commit lên Git
|-- .env.example      # Mẫu cấu hình để chia sẻ với người khác
|-- .gitignore        # Loại bỏ file bí mật và file tạm khỏi Git
|-- llm_client.py     # Đọc cấu hình và gọi Hermes Agent API Server
|-- main.py           # Tạo prompt, gọi hàm LLM và in kết quả
|-- requirements.txt  # Các thư viện Python cần cài
`-- README.md         # Hướng dẫn project
```

## 1. Cài và cấu hình Hermes Agent

Hermes Agent là dịch vụ chạy riêng với project Python này. Trên Windows, có thể
cài bằng Hermes Desktop hoặc chạy lệnh sau trong PowerShell:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Sau khi cài, chọn provider và model bằng trình cấu hình tương tác:

```powershell
hermes model
```

Model/provider thật được cấu hình hoàn toàn bên Hermes. Project Python chỉ gọi
alias OpenAI-compatible được khai báo trong `HERMES_MODEL`.

## 2. Bật Hermes API Server

Thêm các giá trị sau vào file cấu hình môi trường của Hermes (đây không phải
file `.env` của project):

- Windows installer: `%LOCALAPPDATA%\hermes\.env`
- Linux/macOS/WSL: `~/.hermes/.env`

```env
API_SERVER_ENABLED=true
API_SERVER_HOST=127.0.0.1
API_SERVER_PORT=8642
API_SERVER_KEY=change-me-local-dev
```

Giữ API server bind vào `127.0.0.1` khi chỉ dùng trên máy local. API server cho
phép truy cập Hermes Agent, vì vậy hãy dùng key riêng đủ mạnh nếu máy hoặc cổng
có thể được truy cập từ bên ngoài.

Để chỉ thử prompt → response, trong `config.yaml` cùng thư mục cấu hình Hermes,
thêm `api_server: []` vào mục `platform_toolsets` hiện có:

```yaml
platform_toolsets:
  api_server: []
```

Giữ các mục platform khác đang có. Cấu hình này tắt tools cho API server;
cấu hình tools của chat CLI vẫn được giữ nguyên. Khởi động lại gateway sau khi sửa.

## 3. Chạy Hermes gateway

Mở một terminal riêng và chạy:

```powershell
hermes gateway
```

Khi thành công, Hermes sẽ báo API server đang lắng nghe tại:

```text
http://127.0.0.1:8642
```

Có thể kiểm tra nhanh trong PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8642/health
```

Giữ terminal chạy gateway mở trong lúc chạy project.

## 4. Cài project Python

Yêu cầu Python 3.10 trở lên.

### Tạo môi trường ảo

Trên PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Cài thư viện

```powershell
python -m pip install -r requirements.txt
```

### Tạo cấu hình project

Nếu chưa có `.env`, sao chép từ `.env.example`:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Nếu đã có `.env`, cập nhật/thêm ba biến dưới đây. Giữ key local đã cấu hình
khớp với Hermes; không ghi đè bằng key mẫu:

```env
HERMES_BASE_URL=http://127.0.0.1:8642/v1
HERMES_API_KEY=change-me-local-dev
HERMES_MODEL=hermes-agent
```

`HERMES_API_KEY` phải giống `API_SERVER_KEY` trong cấu hình Hermes.
`HERMES_MODEL` là tên model/alias mà Hermes API Server công bố; với profile mặc
định, giá trị thường là `hermes-agent`.

File `.env` đã nằm trong `.gitignore` và không được commit lên Git.

## 5. Chạy chương trình

```powershell
python main.py
```

Nếu gateway đang chạy và cấu hình đúng, phản hồi sẽ được in ngay trong terminal.
Chương trình sẽ hiển thị lỗi dễ hiểu khi không kết nối được gateway, Hermes chưa
chạy, API key sai hoặc response không có content.

## Luồng hoạt động

```text
main.py
   ↓
llm_client.py
   ↓
Hermes Agent API Server
   ↓
model Hermes đang cấu hình
   ↓
response quay lại main.py
```

`main.py` tạo prompt mẫu rồi gọi `get_llm_response(prompt)`. `llm_client.py`
nạp ba biến `HERMES_*`, tạo `OpenAI(base_url=..., api_key=...)`, gọi endpoint
`chat.completions.create()` và trả về content dạng chuỗi cho `main.py`.

Request hiện chỉ gửi `messages` chứa prompt. Project chưa khai báo hoặc xử lý
tool calling.

Để thử prompt khác, chỉ cần sửa biến `prompt` trong `main.py`.

## Tài liệu tham khảo

- [Hermes Agent Quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)
- [Hermes Agent API Server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server)
- [OpenAI Chat API reference](https://developers.openai.com/api/reference/resources/chat)
