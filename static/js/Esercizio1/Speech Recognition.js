// 创建一个SpeechRecognition对象
const recognition = new webkitSpeechRecognition();

// 配置设置以使每次识别都返回连续结果
recognition.continuous = true;

// 配置应返回临时结果的设置
recognition.interimResults = true;

// 正确识别单词或短语时的事件处理程序
recognition.onresult = function (event) {
  console.log(event.results);
};


    window.onload = () => {
      const button = document.getElementById('button');
      button.addEventListener('click', () => {
        if (button.style['animation-name'] === 'flash') {
          recognition.stop();
          button.style['animation-name'] = 'none';
          button.innerText = 'Press to Start';
          content.innerText = '';
        } else {
          button.style['animation-name'] = 'flash';
          button.innerText = 'Press to Stop';
          recognition.start();
        }
      });

      const content = document.getElementById('content');

      const recognition = new webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.onresult = function (event) {
        let result = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          result += event.results[i][0].transcript;
        }
        content.innerText = result;
      };
    };
