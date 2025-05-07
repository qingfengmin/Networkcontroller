async function submitOSPF() {
    try {
        const processId = document.getElementById('ospfProcess').value;
        const areaId = document.getElementById('ospfArea').value;

        const response = await fetch('http://127.0.0.1:5000/api/ospf_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                ospf_process: processId,
                ospf_area: areaId
            })
        });
        
        const data = await response.json();
        document.getElementById('ospfMessage').textContent = data.message;
    } catch (error) {
        console.error('OSPF配置失败:', error);
        document.getElementById('ospfMessage').textContent = '配置提交失败';
    }
}

async function submitBGP() {
    try {
        const asNumber = document.getElementById('bgpAS').value;
        if (!asNumber) {
            document.getElementById('bgpMessage').textContent = '请填写所有必填字段';
            return;
        }

        const response = await fetch('http://127.0.0.1:5000/api/bgp_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                as_number: asNumber,
            })
        });

        const data = await response.json();
        document.getElementById('bgpMessage').textContent = data.message;
    } catch (error) {
        console.error('BGP配置失败:', error);
        document.getElementById('bgpMessage').textContent = '配置提交失败';
    }
}