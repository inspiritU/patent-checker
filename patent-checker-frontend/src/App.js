import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [patentID, setPatentID] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [result, setResult] = useState(null);
  const [savedReports, setSavedReports] = useState([]);

  const handleCheck = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5001/check_infringement', {
        patent_id: patentID,
        company_name: companyName
      });
      setResult(response.data);
    } catch (error) {
      setResult({ error: "No infringing products found." });
    }
  };

  const handleSaveReport = () => {
    if (result && !result.error) {
      setSavedReports([...savedReports, { ...result }]); // Save the entire report
      alert('Report saved successfully!');
    } else {
      alert('No valid report to save.');
    }
  };

  return (
      <div style={styles.container}>
        <h1 style={styles.title}>Patent Infringement Checker</h1>
        <div style={styles.form}>
          <input
              style={styles.input}
              type="text"
              placeholder="Enter Patent ID"
              value={patentID}
              onChange={(e) => setPatentID(e.target.value)}
          />
          <input
              style={styles.input}
              type="text"
              placeholder="Enter Company Name"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
          />
          <button style={styles.button} onClick={handleCheck}>
            Check Infringement
          </button>
        </div>

        {result && (
            <div style={styles.resultContainer}>
              <h2 style={styles.subtitle}>Analysis Result</h2>
              {result.error ? (
                  <p style={styles.error}>{result.error}</p>
              ) : (
                  <div>
                    <p><strong>Patent ID:</strong> {result.patent_id}</p>
                    <p><strong>Company Name:</strong> {result.company_name}</p>
                    <p><strong>Overall Risk Assessment:</strong> {result.overall_risk_assessment}</p>
                    <h3 style={styles.subtitle}>Infringing Products</h3>
                    <ul style={styles.list}>
                      {result.top_infringing_products.map((product, index) => (
                          <li key={index} style={styles.listItem}>
                            <h4>{product.product_name}</h4>
                            <p><strong>Infringement Likelihood:</strong> {product.infringement_likelihood}</p>
                            <p><strong>Relevant Claims:</strong> {product.relevant_claims.join(', ')}</p>
                            <p><strong>Explanation:</strong> {product.explanation}</p>
                            <p><strong>Specific Features:</strong> {product.specific_features.join(', ')}</p>
                          </li>
                      ))}
                    </ul>
                    <button style={styles.saveButton} onClick={handleSaveReport}>
                      Save Report
                    </button>
                  </div>
              )}
            </div>
        )}

        {savedReports.length > 0 && (
            <div style={styles.savedReportsContainer}>
              <h2 style={styles.subtitle}>Saved Reports</h2>
              <ul style={styles.savedReportsList}>
                {savedReports.map((report, index) => (
                    <li key={index} style={styles.savedReportItem}>
                      <h4>Report #{index + 1}</h4>
                      <p><strong>Patent ID:</strong> {report.patent_id}</p>
                      <p><strong>Company Name:</strong> {report.company_name}</p>
                      <p><strong>Overall Risk Assessment:</strong> {report.overall_risk_assessment}</p>
                      <p><strong>Products:</strong></p>
                      <ul style={styles.list}>
                        {report.top_infringing_products.map((product, idx) => (
                            <li key={idx} style={styles.listItem}>
                              <strong>{product.product_name}</strong>
                              <p><strong>Infringement Likelihood:</strong> {product.infringement_likelihood}</p>
                              <p><strong>Relevant Claims:</strong> {product.relevant_claims.join(', ')}</p>
                              <p><strong>Explanation:</strong> {product.explanation}</p>
                              <p><strong>Specific Features:</strong> {product.specific_features.join(', ')}</p>
                            </li>
                        ))}
                      </ul>
                    </li>
                ))}
              </ul>
            </div>
        )}
      </div>
  );
}

const styles = {
  container: {
    fontFamily: "'Arial', sans-serif",
    padding: '20px',
    maxWidth: '800px',
    margin: '0 auto',
    color: '#333',
    backgroundColor: '#f9f9f9',
    borderRadius: '10px',
    boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)'
  },
  title: {
    textAlign: 'center',
    color: '#0056b3',
  },
  subtitle: {
    color: '#333',
    marginBottom: '10px'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    marginBottom: '20px',
  },
  input: {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ccc',
    outline: 'none',
  },
  button: {
    padding: '10px 15px',
    fontSize: '16px',
    backgroundColor: '#0056b3',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  saveButton: {
    padding: '10px 15px',
    fontSize: '16px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    marginTop: '10px',
  },
  resultContainer: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#fff',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  list: {
    padding: '0',
    listStyleType: 'none',
    margin: '10px 0',
  },
  listItem: {
    padding: '10px',
    borderBottom: '1px solid #ddd',
    marginBottom: '10px',
    backgroundColor: '#f5f5f5',
    borderRadius: '5px',
  },
  savedReportsContainer: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#fff',
    borderRadius: '5px',
    border: '1px solid #ccc',
  },
  savedReportsList: {
    padding: '0',
    listStyleType: 'none',
    margin: '10px 0',
  },
  savedReportItem: {
    padding: '10px',
    borderBottom: '1px solid #ddd',
    marginBottom: '10px',
    backgroundColor: '#f5f5f5',
    borderRadius: '5px',
  },
  error: {
    color: '#d9534f',
    fontWeight: 'bold',
  },
};

export default App;
