//从会话存储读取和存储Token

export const getToken = () => {
    // 从 sessionStorage 中读取 token
    const token = sessionStorage.getItem('token');

    if (token) {
        console.log('Token retrieved from sessionStorage:');
        return token;
    } else {
        console.log('No token found in sessionStorage.');
        return null;
    }
}

// 将token存储到浏览器会话存储
export const setToken = (token) => {
    try {
        sessionStorage.setItem('token', token);
        console.log("Token have saved to sessionStorage.")
    } catch (error) {
        console.log("Set token Error: ", error);
    }

}
