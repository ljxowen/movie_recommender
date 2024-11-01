import { LoginService } from "../client/services"

export const loginRequest = async () => {
    try {
        const formData= {
            grant_type: '', // 可以是 'password' 或 null
            username: 'liujingxuanowen@gmail.com', // 必需字段
            password: '0427', // 必需字段
            scope: '', // 默认值为空字符串 
            client_id: null, // 可以是字符串或 null
            client_secret: null, // 可以是字符串或 null
        };

        const response = await LoginService.loginAccessToken({ formData });

        return response;
    } catch (err) {
        throw err;
    }
};