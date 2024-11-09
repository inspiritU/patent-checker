# Patent Infringement Checker

## Project Overview
Patent Infringement Checker is an application based on a Flask backend and React frontend, designed to assess patent infringement risks. The backend uses OpenAI GPT-3.5 to analyze the correlation between product descriptions and patent claims and returns infringement analysis results.

---

## Directory Structure
```
patent-checker/
├── patent-checker-backend/          # Backend code directory
│   ├── app.py                       # Main Flask application file
│   ├── company_products.json        # Company and product data
│   ├── patents.json                 # Patent data
│   └── Dockerfile                   # Backend Docker configuration
├── patent-checker-frontend/         # Frontend code directory
│   ├── src/                         # React source code
│   └── Dockerfile                   # Frontend Docker configuration
├── docker-compose.yml               # Docker Compose configuration
└── README.md                        # Project documentation
```

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-repository.git
cd patent-checker
```

### 2. Configure Environment Variables
Create a `.env` file in the project root directory to store the OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

Ensure the `.env` file contains the following:
- `OPENAI_API_KEY`: Your OpenAI API key.

---

### 3. Start the Services

#### Start with Docker Compose
Run the following command to build and start the project:
```bash
docker-compose up --build
```

Once started:
- **Frontend** is available at: `http://localhost:3000`
- **Backend** is available at: `http://localhost:5001`

---

## How to Use

### 1. Access the Frontend
Open a browser and navigate to [http://localhost:3000](http://localhost:3000). Use the interface to input:
- **Patent ID** (e.g., `US123456`)
- **Company Name** (e.g., `Example Corp`)

Click the **Check Infringement** button to receive the patent infringement analysis results.

### 2. Save Analysis Reports
- On the results page, click **Save Report** to save the current report locally.
- Saved reports will be displayed in the **Saved Reports** section on the page.

---

## Project Features

### Backend API
The backend provides the following main endpoints:
1. **`GET /`**  
   Returns a welcome message.

2. **`POST /check_infringement`**  
   - Request body:
     ```json
     {
       "patent_id": "Patent ID",
       "company_name": "Company Name"
     }
     ```
   - Returns an analysis result, including infringement risks and related product information.

---

## Tech Stack

### Frontend
- **React.js**: Builds the user interface.
- **Axios**: Sends HTTP requests.

### Backend
- **Flask**: Provides the API service.
- **Flask-CORS**: Supports cross-origin requests.
- **OpenAI API**: Uses GPT-3.5 for patent infringement analysis.

### Containerization
- **Docker**: For containerized deployment.
- **Docker Compose**: For managing multi-container services.

---

## Development and Debugging

### Start Backend Locally
1. Navigate to the backend directory:
   ```bash
   cd patent-checker-backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask application:
   ```bash
   python app.py
   ```

The backend runs at `http://127.0.0.1:5000`.

### Start Frontend Locally
1. Navigate to the frontend directory:
   ```bash
   cd patent-checker-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React application:
   ```bash
   npm start
   ```

The frontend runs at `http://localhost:3000`.

---

## TODO
- [ ] Add database support to store analysis records.
- [ ] Provide additional sample data files.
- [ ] Improve frontend styles.
- [ ] Add API documentation.

---

## Troubleshooting

### 1. Docker Container Fails to Start
If there’s a port conflict, modify the port mapping in `docker-compose.yml`. For example:
```yaml
backend:
  ports:
    - "5002:5000"  # Change the host port to 5002
```

Restart the service:
```bash
docker-compose down
docker-compose up --build
```

### 2. OpenAI API Key Not Set
Ensure the `.env` file contains the correct `OPENAI_API_KEY`.

---

## Contact
For any questions, please contact: [olounkle@gmail.com].
