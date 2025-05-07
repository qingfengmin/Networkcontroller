async function submitVxlanForm() {
    try {
        const formData = new FormData(document.getElementById('vxlanForm'));
        const data = {
            address: formData.get('address'),
            mask: formData.get('mask'),
            bd_id: formData.get('bd_id'),
            RD: formData.get('RD'),
            vni: formData.get('vni'),
            import_rt: formData.get('import_rt'),
            export_rt: formData.get('export_rt')
        };

        const response = await fetch('http://127.0.0.1:5000/api/vxlan_gateway', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        document.getElementById('vxlanMessage').textContent = result.message;
        
        if (response.ok) {
            setTimeout(() => {
                window.location.href = 'config.html';
            }, 1500);
        }
    } catch (error) {
        console.error('配置提交失败:', error);
        document.getElementById('vxlanMessage').textContent = '配置提交失败，请检查网络连接';
    }
}