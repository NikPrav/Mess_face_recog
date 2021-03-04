const express = require('express')
const {spawn} = require('child_process');
const app = express()
const path = require('path');
const port = 3000
const bodyParser = require('body-parser');
const fs = require('fs');;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json({limit:'5mb'}));
app.use(bodyParser.raw());

app.post('/recog/', (req, res) => {
    var img = req.body.image.split(',')[1]
    let buff = new Buffer(img, 'base64')
    fs.writeFileSync('pic1.png', buff);

 
 var dataToSend;
 // spawn new child process to call the python script
 const python = spawn('python', ['recognize.py','pic1.png','True']);
 // collect data from script
 python.stdout.on('data', function (data) {
  console.log('Pipe data from python script ...');
  dataToSend = data.toString();
 });
 // in close event we are sure that stream from child process is closed
 python.on('close', (code) => {
 console.log(`child process close all stdio with code ${code}`);
 // send data to browser
 
 console.log(dataToSend)
// [TODO] wrap this int a json respone
 res.send(dataToSend)
 });
 
})

app.post('/test2/',(req,res) => {
    // console.log(req.body)
    var img = req.body.image.split(',')[1]
    let buff = new Buffer(img, 'base64')
    fs.writeFileSync('pic1.png', buff);

    res.sendStatus(200)
})

app.use('/', function(req,res){
    res.sendFile(path.join(__dirname+'/express/index.html'));
    //__dirname : It will resolve to your project folder.
});


app.listen(port, () => console.log(`Example app listening on port 
${port}!`))