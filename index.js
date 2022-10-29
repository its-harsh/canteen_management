const { app, BrowserWindow, ipcMain } = require('electron');
const axios = require('axios');
const path = require('path')

var auth_token = '';
var username = '';


function showWindow() {
    // creating window 
    let win = new BrowserWindow({
        width: 1000,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, "preload.js")
        },
    });
    // loding login.html
    win.loadFile('desktop-app-templates/login.html');
    // got event from login.html
    ipcMain.on('login-request', (event, arg) => {
        username = arg.username;
        // sending post request login
        axios.post('http://127.0.0.1:8000/api-auth/auth-token/', arg)
            .then((res) => {
                auth_token = res.data.token;
                console.log(auth_token)
                showdashboardWindow();
                win.close();
            })
            .catch((err) => { console.log(err) });
    });
    // handeling event from main.js
    ipcMain.on('registeration-request-form', () => {
        showRegisteration();
        win.close();
    });
    // optimising memory on window closed
    win.on('closed', () => {
        win = null;
    });
}


function showRegisteration() {
    let win = new BrowserWindow({
        width: 1000,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, "preload.js")
        }
    });

    win.loadFile('desktop-app-templates/register.html');
    // handeling event from registeration
    ipcMain.on('registeration-request', (event, arg) => {
        // sending post request to register user
        axios.post('http://127.0.0.1:8000/api-auth/auth/', arg)
            .then((res) => {
                auth_token = res.data.token;
                username = res.data.username;
                showdashboardWindow();
                win.close();
            })
            .catch((err) => { console.log(err) });
    });

    win.on('closed', () => {
        win = null;
    });
}


function showdashboardWindow() {
    let win = new BrowserWindow({
        width: 1000,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            enableRemoteModule: false,
            preload: path.join(__dirname, "preload.js")
        }
    });

    win.loadFile('desktop-app-templates/dashboard.html');
    win.webContents.on('did-finish-load', () => {
        // calling user details api
        axios.get(`http://127.0.0.1:8000/api-auth/auth/${username}`, { headers: { 'Authorization': `token ${auth_token}` } })
            .then((res) => {
                // send event to dashboard.html
                win.webContents.send('user-detail', res.data);
            })
            .catch((err) => { console.log(err) });

        axios.get(`http://127.0.0.1:8000/api/`, { headers: { 'Authorization': `token ${auth_token}` } })
            .then((res) => {
                // send event to dashboard.html
                win.webContents.send('all-food-detail', res.data);
            })
            .catch((err) => { console.log(err) });
    });
    // handeling event from dashbord.html
    ipcMain.on('order', (event, post_request_arg) => {
        axios.post('http://127.0.0.1:8000/api/user_order/order/', post_request_arg, { headers: { 'Authorization': `token ${auth_token}` } })
            .then((res) => {
                win.loadFile('desktop-app-templates/display_order.html');
                win.webContents.on('did-finish-load', () => {
                    axios.get(`http://127.0.0.1:8000/api/user_order/${res.data.id}/`, { headers: { 'Authorization': `token ${auth_token}` } })
                        .then((res) => {
                            //sending event to display_order.html
                            win.webContents.send('order-data', res.data);
                        })
                        .catch((err) => { console.log(err) });
                })
            })
            .catch((err) => { console.log(err) });
    });

    win.on('closed', () => {
        win = null;
    });
}

app.on('ready', showWindow);

app.on('window-all-closed', () => {
    app.quit();
});
