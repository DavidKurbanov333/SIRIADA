import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import {
    Box,
    Button,
    Container,
    TextField,
    Typography,
    Paper,
    Alert,
    CircularProgress,
    IconButton,
    InputAdornment
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import config from '../config';

const validationSchema = yup.object({
    password: yup
        .string()
        .min(8, 'Пароль должен содержать минимум 8 символов')
        .required('Пароль обязателен'),
    confirmPassword: yup
        .string()
        .oneOf([yup.ref('password')], 'Пароли должны совпадать')
        .required('Подтверждение пароля обязательно'),
});

interface PasswordFormData {
    password: string;
    confirmPassword: string;
}

const PasswordForm: React.FC = () => {
    const navigate = useNavigate();
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const formik = useFormik<PasswordFormData>({
        initialValues: {
            password: '',
            confirmPassword: '',
        },
        validationSchema: validationSchema,
        onSubmit: async (values) => {
            setLoading(true);
            setError(null);
            
            try {
                // Получаем сохраненные данные пользователя
                const userData = JSON.parse(localStorage.getItem('userData') || '{}');
                console.log('Отправляемые данные:', { ...userData, password: '***' });
                
                // Отправляем данные на сервер
                const response = await fetch(`${config.apiUrl}/users/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                    },
                    body: JSON.stringify({
                        ...userData,
                        password: values.password
                    }),
                });

                console.log('Статус ответа:', response.status);
                const data = await response.json();
                console.log('Ответ сервера:', data);

                if (!response.ok) {
                    throw new Error(data.detail || `Ошибка сервера: ${response.status}`);
                }

                // Очищаем данные из localStorage
                localStorage.removeItem('userData');
                
                // Перенаправляем на страницу профиля
                navigate(`/profile/${data.user_id}`);
            } catch (err) {
                console.error('Ошибка при регистрации:', err);
                if (err instanceof Error) {
                    setError(err.message);
                } else if (typeof err === 'string') {
                    setError(err);
                } else {
                    setError('Произошла неизвестная ошибка при регистрации');
                }
            } finally {
                setLoading(false);
            }
        },
    });

    return (
        <Container maxWidth="sm">
            <Paper elevation={3} sx={{ p: 4, mt: 4, backgroundColor: '#ffffff' }}>
                <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ color: '#1976d2', mb: 4 }}>
                    Создание пароля
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 3 }}>
                        {error}
                    </Alert>
                )}

                <Box component="form" onSubmit={formik.handleSubmit} sx={{ mt: 2 }}>
                    <TextField
                        fullWidth
                        id="password"
                        name="password"
                        label="Пароль"
                        type={showPassword ? 'text' : 'password'}
                        value={formik.values.password}
                        onChange={formik.handleChange}
                        error={formik.touched.password && Boolean(formik.errors.password)}
                        helperText={formik.touched.password && formik.errors.password}
                        sx={{ mb: 3 }}
                        variant="outlined"
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        onClick={() => setShowPassword(!showPassword)}
                                        edge="end"
                                    >
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />

                    <TextField
                        fullWidth
                        id="confirmPassword"
                        name="confirmPassword"
                        label="Подтвердите пароль"
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={formik.values.confirmPassword}
                        onChange={formik.handleChange}
                        error={formik.touched.confirmPassword && Boolean(formik.errors.confirmPassword)}
                        helperText={formik.touched.confirmPassword && formik.errors.confirmPassword}
                        sx={{ mb: 4 }}
                        variant="outlined"
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                                        edge="end"
                                    >
                                        {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            ),
                        }}
                    />

                    <Button
                        color="primary"
                        variant="contained"
                        fullWidth
                        type="submit"
                        size="large"
                        disabled={loading}
                        sx={{ 
                            py: 1.5,
                            fontSize: '1.1rem',
                            textTransform: 'none',
                            boxShadow: 2,
                            '&:hover': {
                                boxShadow: 4
                            }
                        }}
                    >
                        {loading ? <CircularProgress size={24} color="inherit" /> : 'Зарегистрироваться'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};

export default PasswordForm; 