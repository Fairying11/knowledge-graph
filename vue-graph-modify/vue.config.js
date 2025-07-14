// http://127.0.0.1:5000/star/attribute
module.exports = {
  devServer: {
    open: true,
    host: 'localhost',
    port: 8080,
    https: false,
	// proxy:'http://192.168.182.1:5000'
    // 以上的ip和端口是我们本机的;下面为需要跨域的
    proxy: { // 配置跨域
		
      '/star': {
        target: 'http://192.168.182.1:5000', // 这里后台的地址模拟的;应该填写你们真实的后台接口
      },
	  '/relationship': {
	    target: 'http://192.168.182.1:5001', // 这里后台的地址模拟的;应该填写你们真实的后台接口
	  }
    }
  }
}
