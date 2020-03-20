const bodyParser = require("body-parser");
const CryptoJS = require("crypto-js");
const express = require("express");
const axios = require('axios');
var cors = require('cors');
var atob = require('atob');

const app = express();
const whitelist = ['www.equishell.com', "https://www.equishell.com", "*"];
var corsOptionsDelegate = (req, callback) => {
    let corsOptions = {
        allowedMethods: ["POST"],
        allowedHeaders: ["Content-Type", "Authorization"],
    };
    if (whitelist.indexOf(req.header('Origin')) !== -1||whitelist.indexOf("*") !== -1) {
      corsOptions['origin'] = true // reflect (enable) the requested origin in the CORS response
    } else {
        corsOptions['origin'] = false // disable CORS for thi.s request
    }
    callback(null, corsOptions); // callback expects two parameters: error and options
}

app.use(cors(corsOptionsDelegate));

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.json());

const server = app.listen(9020, "127.0.0.1");

// Socket IO Connection
const io = require("./socket").init(server);

io.on("connection", socket=>{
    console.log(socket.client.conn.server.clientsCount);
    socket.on("message", data=>{
        axios.post('http://127.0.0.1:9013/success/',{
            "message": data.message
        }).then(res=>{
            data = JSON.parse(atob(res.data));
            console.log(data);
            answerHash = CryptoJS.RabbitLegacy.encrypt(JSON.stringify(data), "HobjShtfaLthqyFF35w1UwKhfz6IceeY6XpmF6a0fovNYmPBXE+QpWiFiGNOVwfoaWWmsknSGlPHywctskkKXQ==").toString();
            socket.emit("answers", answerHash);
        }).catch(err=>{
            console.error("Error", err);
        });
        // let start = new Date().getTime();
        // let answer = equiCore(data.message.toLowerCase());
        // let end = new Date().getTime();
        // answerDisct = {answer: answer, time: (end-start)};
        // let log = logRequest({data: data, answer: answerDisct});
        // answerHash = CryptoJS.RabbitLegacy.encrypt(JSON.stringify(answerDisct), "HobjShtfaLthqyFF35w1UwKhfz6IceeY6XpmF6a0fovNYmPBXE+QpWiFiGNOVwfoaWWmsknSGlPHywctskkKXQ==").toString();
        // console.log(answerDisct)
        // socket.emit("answers", answerHash);
    });
});

async function logRequest (data) {
    // save to mongodb
    return 200;
}