module.exports = {
  apps: [
    {
      name: 'ai-employee-orchestrator',
      script: 'python',
      args: 'orchestrator.py',
      cwd: 'F:/DigitalFTEwithClaude',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'development'
      },
      error_file: './logs/pm2-orchestrator-error.log',
      out_file: './logs/pm2-orchestrator-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    },
    {
      name: 'ai-employee-filesystem-watcher',
      script: 'python',
      args: 'filesystem_watcher.py',
      cwd: 'F:/DigitalFTEwithClaude',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'development'
      },
      error_file: './logs/pm2-filesystem-watcher-error.log',
      out_file: './logs/pm2-filesystem-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    },
    {
      name: 'ai-employee-gmail-watcher',
      script: 'python',
      args: 'gmail_watcher.py',
      cwd: 'F:/DigitalFTEwithClaude',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'development'
      },
      error_file: './logs/pm2-gmail-watcher-error.log',
      out_file: './logs/pm2-gmail-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    },
    {
      name: 'ai-employee-whatsapp-watcher',
      script: 'python',
      args: 'whatsapp_watcher.py',
      cwd: 'F:/DigitalFTEwithClaude',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'development'
      },
      error_file: './logs/pm2-whatsapp-watcher-error.log',
      out_file: './logs/pm2-whatsapp-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    },
    {
      name: 'ai-employee-linkedin-watcher',
      script: 'python',
      args: 'linkedin_watcher.py',
      cwd: 'F:/DigitalFTEwithClaude',
      instances: 1,
      autorestart: false,  // Changed to false to prevent rapid restarts when authentication fails
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'development'
      },
      error_file: './logs/pm2-linkedin-watcher-error.log',
      out_file: './logs/pm2-linkedin-watcher-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss'
    }
  ]
};
