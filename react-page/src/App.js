import React, { Fragment } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import { CameraFeed } from './components/camera-feed';
import './App.css';

// Upload to local seaweedFS instance
const uploadImage = async file => { 
  // alert(1)
  // const formData = new FormData();
  // formData.append('file', file);
  // console.log(file)
  var reader = new FileReader();
  reader.readAsDataURL(file); 
  reader.onloadend = function() {
    var base64data = reader.result;                
    console.log(base64data);
    // Simple POST request with a JSON body using fetch
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: base64data })
    };
    fetch('http://localhost:3000/recog', requestOptions)
      .then(response => response.text())
      .then(data => {console.log(data)});
  
    }

  // Connect to a seaweedfs instance
};

function App() {
  return (
    <div className="App">
        <h1>Image capture test</h1>
        <p>Capture image from USB webcamera and upload to form</p>
        <CameraFeed sendFile={uploadImage} />
    </div>
);
}

export default App;
