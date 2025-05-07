async function initDevice() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/device_init', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ True: true })
        });
        const data = await response.json();
        document.getElementById('initMessage').textContent = data.message;
    } catch (error) {
        console.error('初始化失败:', error);
        document.getElementById('initMessage').textContent = '初始化配置失败';
    }
}

async function mustConfig() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/device_must', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ True: true })
        });
        const data = await response.json();
        document.getElementById('mustMessage').textContent = data.message;
    } catch (error) {
        console.error('必须配置失败:', error);
        document.getElementById('mustMessage').textContent = '必须配置失败';
    }
}

async function connectAddress() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/device_connect_address', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ True: true })
        });
        const data = await response.json();
        document.getElementById('connectMessage').textContent = data.message;
    } catch (error) {
        console.error('连接配置失败:', error);
        document.getElementById('connectMessage').textContent = '连接地址配置失败';
    }
}