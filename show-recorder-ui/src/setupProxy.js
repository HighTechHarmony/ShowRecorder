const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:5000", // Backend server
      changeOrigin: true, // Changes the origin of the host header to the target URL
    })
  );
};