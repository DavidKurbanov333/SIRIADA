import React, { useEffect, useState } from 'react';
import {
    Box,
    Container,
    Paper,
    Typography,
    CircularProgress,
    Alert
} from '@mui/material';
import { useParams } from 'react-router-dom';

interface UserProfile {
    user_id: string;
    birth_year: number;
    city: string;
    gender: string;
    citizenship: string;
    registration_date: string;
}

const UserProfile: React.FC = () => {
    const { userId } = useParams<{ userId: string }>();
    const [user, setUser] = useState<UserProfile | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch(`http://localhost:8000/users/${userId}`);
                if (!response.ok) {
                    throw new Error('Пользователь не найден');
                }
                const data = await response.json();
                setUser(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Произошла ошибка при загрузке данных');
            } finally {
                setLoading(false);
            }
        };

        if (userId) {
            fetchUserData();
        }
    }, [userId]);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Container maxWidth="sm">
                <Alert severity="error" sx={{ mt: 4 }}>
                    {error}
                </Alert>
            </Container>
        );
    }

    if (!user) {
        return null;
    }

    return (
        <Container maxWidth="sm">
            <Paper elevation={3} sx={{ p: 4, mt: 4, backgroundColor: '#ffffff' }}>
                <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ color: '#1976d2', mb: 4 }}>
                    Личный кабинет
                </Typography>
                
                <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" color="primary" gutterBottom>
                        Ваш ID:
                    </Typography>
                    <Typography variant="h4" sx={{ 
                        fontFamily: 'monospace',
                        backgroundColor: '#f5f5f5',
                        p: 2,
                        borderRadius: 1,
                        textAlign: 'center',
                        letterSpacing: 2
                    }}>
                        {user.user_id}
                    </Typography>
                </Box>

                <Box sx={{ mt: 4 }}>
                    <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                        Основная информация:
                    </Typography>
                    <Box sx={{ pl: 2 }}>
                        <Typography variant="body1" sx={{ mb: 1 }}>
                            Год рождения: {user.birth_year}
                        </Typography>
                        <Typography variant="body1" sx={{ mb: 1 }}>
                            Город: {user.city}
                        </Typography>
                        <Typography variant="body1" sx={{ mb: 1 }}>
                            Пол: {user.gender}
                        </Typography>
                        <Typography variant="body1" sx={{ mb: 1 }}>
                            Гражданство: {user.citizenship}
                        </Typography>
                        <Typography variant="body1" sx={{ mb: 1 }}>
                            Дата регистрации: {new Date(user.registration_date).toLocaleDateString()}
                        </Typography>
                    </Box>
                </Box>
            </Paper>
        </Container>
    );
};

export default UserProfile; 