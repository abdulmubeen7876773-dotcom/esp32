const fs = require('fs');
const http = require('http');
const path = require('path');

const contentTypes = new Map([
  ['.css', 'text/css; charset=utf-8'],
  ['.gif', 'image/gif'],
  ['.html', 'text/html; charset=utf-8'],
  ['.ico', 'image/x-icon'],
  ['.jpg', 'image/jpeg'],
  ['.jpeg', 'image/jpeg'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.json', 'application/json; charset=utf-8'],
  ['.png', 'image/png'],
  ['.svg', 'image/svg+xml; charset=utf-8'],
  ['.txt', 'text/plain; charset=utf-8'],
  ['.webp', 'image/webp'],
  ['.xml', 'application/xml; charset=utf-8'],
]);

function createStaticServer(options = {}) {
  const host = options.host || process.env.HOST || '127.0.0.1';
  const port = Number(options.port || process.env.PORT || 4173);
  const root = path.resolve(options.root || path.join(__dirname, '..'));

  function resolveRequestPath(requestUrl) {
    const url = new URL(requestUrl, `http://${host}:${port}`);
    let pathname = decodeURIComponent(url.pathname);
    if (pathname.endsWith('/')) {
      pathname += 'index.html';
    }

    const filePath = path.resolve(root, `.${pathname}`);
    if (filePath !== root && !filePath.startsWith(`${root}${path.sep}`)) {
      return null;
    }

    return filePath;
  }

  function sendFile(req, res, filePath) {
    fs.stat(filePath, (statError, stat) => {
      if (statError || !stat.isFile()) {
        res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end('Not found');
        return;
      }

      const headers = {
        'Content-Length': stat.size,
        'Content-Type': contentTypes.get(path.extname(filePath).toLowerCase()) || 'application/octet-stream',
      };

      res.writeHead(200, headers);
      if (req.method === 'HEAD') {
        res.end();
        return;
      }

      fs.createReadStream(filePath).pipe(res);
    });
  }

  const server = http.createServer((req, res) => {
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      res.writeHead(405, { Allow: 'GET, HEAD' });
      res.end();
      return;
    }

    const filePath = resolveRequestPath(req.url);
    if (!filePath) {
      res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('Forbidden');
      return;
    }

    sendFile(req, res, filePath);
  });

  const sockets = new Set();
  server.on('connection', (socket) => {
    sockets.add(socket);
    socket.on('close', () => sockets.delete(socket));
  });

  return {
    listen() {
      return new Promise((resolve, reject) => {
        function onError(error) {
          reject(error);
        }

        server.once('error', onError);
        server.listen(port, host, () => {
          server.off('error', onError);
          console.log(`Serving ${root} at http://${host}:${port}`);
          resolve();
        });
      });
    },

    close() {
      return new Promise((resolve) => {
        if (!server.listening) {
          resolve();
          return;
        }

        server.close(() => resolve());
        server.closeIdleConnections?.();
        server.closeAllConnections?.();
        for (const socket of sockets) {
          socket.destroy();
        }
      });
    },
  };
}

module.exports = { createStaticServer };

if (require.main === module) {
  const staticServer = createStaticServer();

  staticServer.listen().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });

  for (const signal of ['SIGBREAK', 'SIGHUP', 'SIGINT', 'SIGTERM']) {
    process.on(signal, () => {
      staticServer.close().catch((error) => {
        console.error(error);
        process.exitCode = 1;
      });
    });
  }
}
