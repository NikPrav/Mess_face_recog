import React, { useState } from 'react';
import { CameraFeed } from './components/camera-feed';
import './App.css';
var personname = 'ab'
// import { ThemeProvider } from "@chakra-ui/core"
// Upload to local seaweedFS instance


function App() {
  const uploadImage = async file => { 
    // alert(1)
    // const formData = new FormData();
    // formData.append('file', file);
    // console.log(file)
    var reader = new FileReader();
    reader.readAsDataURL(file); 
    reader.onloadend = function() {
      var base64data = reader.result;                
      // console.log(base64data);
      // Simple POST request with a JSON body using fetch
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: base64data })
      };
      fetch('http://localhost:3001/recog', requestOptions)
        .then(response => response.text())
        .then(data => {setData(data)});
  
  
      }
  
    // Connect to a seaweedfs instance
  };
  const [message, setData] = useState("loading...")
  return (
    <div className="App">
        <h1>Image capture test</h1>
        <p>Capture image from USB webcamera and upload to form</p>
        <CameraFeed sendFile={uploadImage} />
        <p>{message}</p>
    </div>
);
}

export default App;
