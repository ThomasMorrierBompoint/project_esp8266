module.exports = {
  apps: [
    {
      name: 'app',
      script: './server.js',
      log_file: './log/combined.log',
      log_date_format: 'HH:mm',
    },
  ],
};
