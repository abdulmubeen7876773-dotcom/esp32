const { createStaticServer } = require('./static-server.cjs');

module.exports = async () => {
  const staticServer = createStaticServer();
  await staticServer.listen();

  return async () => {
    await staticServer.close();
  };
};
