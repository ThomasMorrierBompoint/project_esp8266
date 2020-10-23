/**
 * Module dependencies.
 */
const shell = require('shelljs');
const fs = require('fs-extra');
const path = require('path');
const cors = require('cors');
const morgan = require('morgan');
const express = require('express');
const bodyParser = require('body-parser');
const compression = require('compression');
const errorHandler = require('errorhandler');
const expressStatusMonitor = require('express-status-monitor');

const ESP8266_PORT = '/dev/ttyUSB0';

/**
 * Create Express server.
 */
const app = express();

/**
 * Express configuration.
 */
app.set('port', process.env.PORT || 8000);
app.use(morgan('dev'));
app.use(expressStatusMonitor());
app.use(compression());
app.use(cors());

/**
 * Static file Handler.
 */
app.use('/', express.static(path.join(__dirname, 'public'), { maxAge: 1000 * 60 * 60 * 24 * 365 }));

/**
 * POST data parser.
 */
app.use(bodyParser.json({ type: 'application/json', limit: '5000kb', extended: true }));

/**
 * Routes.
 */
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'public/index.html')));

app.get('/:action', (req, res) => {
  const shellExec = (command) => {
    result = shell.exec(command);
    if (result.code !== 0) {
      errors.push(result);
    } else {
      results.push(result);
    }
  };

  const { action } = req.params;
  const commands = {
    debug: [`echo "\n***** SERIAL PORT *****" && dmesg | grep tty && echo "\n"`, `ampy --port ${ESP8266_PORT} run dist/debug.py`],
    // reset: [`ampy --port ${ESP8266_PORT} reset`, `ampy --port ${ESP8266_PORT} ls`],
    reset: [`ampy --port ${ESP8266_PORT} ls`],
  };

  let results = [];
  let errors = [];
  let result;

  commands[action].forEach((c) => shellExec(c));
  if (action === 'reset') {
    const libs = fs.readdirSync('pyboard');
    const files = results.slice(-1)[0].stdout.split('\n');
    files.forEach((f) => f && shellExec(`ampy --port ${ESP8266_PORT} rm /${f}`));
    libs.forEach((f) => shellExec(`ampy --port ${ESP8266_PORT} put pyboard/${f}`));
    shellExec(`ampy --port ${ESP8266_PORT} reset`);
  }

  errors = errors.map((e) => e.stderr);
  results = results.map((r) => r.stdout);

  if (errors.length) {
    res.send({ code: 'ERROR', errors, results });
  } else {
    res.send({ code: 'SUCCESS', results });
  }
});

app.post('/upload-file-and-run', (req, res) => {
  const { code } = req.body;
  const main = 'dist/server-esp8266-script.py';

  fs.writeFile(main, code, async (err) => {
    if (err) {
      return res.send({ code: 'ERROR', err });
    }
    const result = shell.exec(`ampy --port ${ESP8266_PORT} run ${main}`);
    if (result.code !== 0) {
      res.send({ code: 'ERROR', errors: [result.stderr] });
    } else {
      res.send({ code: 'SUCCESS', results: [result.stdout] });
    }
  });
});

/**
 * 404 Handler (Always return the Vue.js App).
 */
app.all('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/index.html'));
});

/**
 * Error Handler.
 */
app.use(errorHandler());

/**
 * Start Express server.
 */
app.listen(app.get('port'), () => {
  console.log('App is running on port: %d in %s mode', app.get('port'), app.get('env'));
});
