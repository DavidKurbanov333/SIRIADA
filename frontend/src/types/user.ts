export enum City {
    YAROSLAVL = "Ярославль",
    MOSCOW = "Москва/МО",
    SPB = "Санкт-Петербург/ЛО"
}

export enum Gender {
    MALE = "мужской",
    FEMALE = "женский"
}

export enum Citizenship {
    RF = "РФ",
    CIS = "СНГ",
    OTHER = "другое"
}

export interface User {
    user_id: string;
    birth_year: number;
    city: string;
    gender: string;
    citizenship: string;
    phone_number: string;
    registration_date: string;
}

export interface UserFormData {
    birth_year: number;
    city: City;
    gender: Gender;
    citizenship: Citizenship;
    phone_number: string;
} 