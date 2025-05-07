// 模拟设备列表
let devices = [];

// 添加设备函数
async function addDevice() {
    const deviceName = document.getElementById('deviceName').value;
    const deviceType = document.getElementById('deviceType').value;

    if (deviceName === '') {
        alert('请输入设备名称');
        return;
    }

    const newDevice = {
        device_ip: deviceName,
        device_type: deviceType
    };

    // 发送请求到后端添加设备
    try {
        const response = await fetch('http://127.0.0.1:5000/api/add_device', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newDevice)
        });
        const data = await response.json();
        if (data.message === '设备添加成功') {
            devices.push(newDevice);
            displayDevices();
            document.getElementById('deviceName').value = '';
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('添加设备失败:', error);
        alert('添加设备失败，请稍后重试');
    }
}

// 显示设备列表函数
function displayDevices() {
    const deviceList = document.getElementById('deviceList');
    deviceList.innerHTML = '';

    devices.forEach((device, index) => {
        const listItem = document.createElement('li');
        listItem.classList.add('flex', 'items-center', 'justify-between', 'border-b', 'border-gray-300', 'py-2');
        listItem.innerHTML = `
            <span>${device.device_ip} - ${device.device_type}</span>
            <button onclick="deleteDevice(${index})" class="bg-red-500 text-white py-1 px-2 rounded hover:bg-red-600">删除</button>
        `;
        deviceList.appendChild(listItem);
    });
}

// 删除设备函数
async function deleteDevice(index) {
    const device = devices[index];

    // 发送请求到后端删除设备
    try {
        const response = await fetch('http://127.0.0.1:5000/api/del_device', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ device_ip: device.device_ip })
        });
        const data = await response.json();
        if (data.message === '设备删除成功') {
            devices.splice(index, 1);
            displayDevices();
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('删除设备失败:', error);
        alert('删除设备失败，请稍后重试');
    }
}

// 页面加载时显示设备列表
displayDevices();