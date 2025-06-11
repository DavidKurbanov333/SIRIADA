import React from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import {
    Box,
    Button,
    Container,
    FormControl,
    FormHelperText,
    InputLabel,
    MenuItem,
    Select,
    TextField,
    Typography,
    Paper
} from '@mui/material';
import { UserFormData, City, Gender, Citizenship } from '../types/user';
import { useNavigate } from 'react-router-dom';

const validationSchema = yup.object({
    birth_year: yup
        .number()
        .required('Год рождения обязателен')
        .min(1900, 'Некорректный год рождения')
        .max(new Date().getFullYear() - 18, 'Вам должно быть 18 лет или больше'),
    city: yup
        .string()
        .oneOf(Object.values(City), 'Выберите город из списка')
        .required('Город обязателен'),
    gender: yup
        .string()
        .oneOf(Object.values(Gender), 'Выберите пол')
        .required('Пол обязателен'),
    citizenship: yup
        .string()
        .oneOf(Object.values(Citizenship), 'Выберите гражданство')
        .required('Гражданство обязательно'),
    phone_number: yup
        .string()
        .required('Номер телефона обязателен')
        .matches(/^[78]\d{10}$/, 'Введите корректный номер телефона'),
});

const UserForm: React.FC = () => {
    const navigate = useNavigate();

    const formik = useFormik<UserFormData>({
        initialValues: {
            birth_year: new Date().getFullYear() - 18,
            city: City.MOSCOW,
            gender: Gender.MALE,
            citizenship: Citizenship.RF,
            phone_number: '',
        },
        validationSchema: validationSchema,
        onSubmit: (values) => {
            localStorage.setItem('userData', JSON.stringify(values));
            navigate('/password');
        },
    });

    return (
        <Container maxWidth="sm">
            <Paper elevation={3} sx={{ 
                p: 4, 
                mt: 4, 
                backgroundColor: '#ffffff',
                borderRadius: 2,
                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
            }}>
                <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ 
                    color: '#1a237e',
                    mb: 4,
                    fontWeight: 500
                }}>
                    Анкета
                </Typography>
                <Typography variant="subtitle1" gutterBottom align="center" sx={{ mb: 4, color: '#666' }}>
                    Заполните поля ниже:
                </Typography>
                
                <Box component="form" onSubmit={formik.handleSubmit} sx={{ mt: 2 }}>
                    <TextField
                        fullWidth
                        id="phone_number"
                        name="phone_number"
                        label="Номер телефона"
                        value={formik.values.phone_number}
                        onChange={formik.handleChange}
                        error={formik.touched.phone_number && Boolean(formik.errors.phone_number)}
                        helperText={formik.touched.phone_number && formik.errors.phone_number}
                        sx={{ mb: 3 }}
                        variant="outlined"
                        placeholder="+7 (___) ___-__-__"
                    />

                    <TextField
                        fullWidth
                        id="birth_year"
                        name="birth_year"
                        label="Год рождения"
                        type="number"
                        value={formik.values.birth_year}
                        onChange={formik.handleChange}
                        error={formik.touched.birth_year && Boolean(formik.errors.birth_year)}
                        helperText={formik.touched.birth_year && formik.errors.birth_year}
                        sx={{ mb: 3 }}
                        variant="outlined"
                    />

                    <FormControl fullWidth error={formik.touched.citizenship && Boolean(formik.errors.citizenship)} sx={{ mb: 3 }}>
                        <InputLabel>Ваше гражданство</InputLabel>
                        <Select
                            id="citizenship"
                            name="citizenship"
                            value={formik.values.citizenship}
                            label="Ваше гражданство"
                            onChange={formik.handleChange}
                            variant="outlined"
                        >
                            {Object.values(Citizenship).map((citizenship) => (
                                <MenuItem key={citizenship} value={citizenship}>
                                    {citizenship}
                                </MenuItem>
                            ))}
                        </Select>
                        {formik.touched.citizenship && formik.errors.citizenship && (
                            <FormHelperText>{formik.errors.citizenship}</FormHelperText>
                        )}
                    </FormControl>

                    <FormControl fullWidth error={formik.touched.city && Boolean(formik.errors.city)} sx={{ mb: 3 }}>
                        <InputLabel>Город проживания</InputLabel>
                        <Select
                            id="city"
                            name="city"
                            value={formik.values.city}
                            label="Город проживания"
                            onChange={formik.handleChange}
                            variant="outlined"
                        >
                            {Object.values(City).map((city) => (
                                <MenuItem key={city} value={city}>
                                    {city}
                                </MenuItem>
                            ))}
                        </Select>
                        {formik.touched.city && formik.errors.city && (
                            <FormHelperText>{formik.errors.city}</FormHelperText>
                        )}
                    </FormControl>

                    <FormControl fullWidth error={formik.touched.gender && Boolean(formik.errors.gender)} sx={{ mb: 4 }}>
                        <InputLabel>Ваш пол</InputLabel>
                        <Select
                            id="gender"
                            name="gender"
                            value={formik.values.gender}
                            label="Ваш пол"
                            onChange={formik.handleChange}
                            variant="outlined"
                        >
                            {Object.values(Gender).map((gender) => (
                                <MenuItem key={gender} value={gender}>
                                    {gender}
                                </MenuItem>
                            ))}
                        </Select>
                        {formik.touched.gender && formik.errors.gender && (
                            <FormHelperText>{formik.errors.gender}</FormHelperText>
                        )}
                    </FormControl>

                    <Button
                        color="primary"
                        variant="contained"
                        fullWidth
                        type="submit"
                        size="large"
                        sx={{ 
                            py: 1.5,
                            fontSize: '1.1rem',
                            textTransform: 'none',
                            boxShadow: 2,
                            backgroundColor: '#1a237e',
                            '&:hover': {
                                backgroundColor: '#283593',
                                boxShadow: 4
                            }
                        }}
                    >
                        Отправить
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};

export default UserForm; 