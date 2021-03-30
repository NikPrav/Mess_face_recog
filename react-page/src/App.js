import React, { useState } from 'react';
import { Box } from "@chakra-ui/react";
// import { extendTheme } from "@chakra-ui/react"
import { CameraFeed } from './components/camera-feed';
import './App.css';
var personname = 'ab'
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
        body: JSON.stringify({ image: base64data, transform: 'data_transforms' })
      };
      fetch('http://localhost:5000/pictest', requestOptions)
        .then(response => response.text())
        .then(data => {setData(data)});
  
  
      }
  
    // Connect to a seaweedfs instance
  };
  const [message, setData] = useState("loading...")
  return (
    <div>
       <Box  m="8px" p="12px" w="900px" h="1100px"  textAlign="center" fontFamily="Arial" rounded="10px" borderColor="gray.300" boxShadow="md" bg="lavender">
       <h1>Image capture test</h1>
       <p>Capture image from USB webcamera and upload to form</p>
        <CameraFeed sendFile={uploadImage} />
        <p>{message}</p>
      </Box>
        
    </div>
);
}

export default App;
