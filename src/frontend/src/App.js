import './App.css';
import React, {useState} from 'react'

function App() {
  const[inputText, setInputText] = useState('')
  const[responseText, setResponseText] = useState([])

  //Set input text variable to value from text box
  const handleChange = (event) => {
    setInputText(event.target.value);
  };

  //Event to occur on click of submit button
  const handleSubmit = (event) => {
    event.preventDefault();

    // Send POST request to the backend
    fetch('/run_rag', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ data: inputText }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        setResponseText(data.split('\n'));
        setInputText('');
      })
      .catch((error) => {
        console.error('Error:', error);
      });
      document.getElementById("text-box").value = "";
  };

  //HTML setup for homepage
  return (
    <div className="container">
      <div className="title-area">
        <h1>Find Product Instructions</h1>
      </div>
      <div className="content-area">
        <form className="input-form" onSubmit={handleSubmit}>
          <input 
            id='text-box'
            type="text" 
            placeholder="Enter Product" 
            value={inputText}
            onChange={handleChange} 
          />
          <button type="submit">Submit</button>
        </form>
      </div>
      {responseText.length > 0 && (
        <div className="answer-area">
          {responseText.map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
      )}
    </div>
  );
};


export default App;
