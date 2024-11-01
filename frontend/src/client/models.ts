export type Body_______login_login_access_token = {
	grant_type?: string | null;
	username: string;
	password: string;
	scope?: string;
	client_id?: string | null;
	client_secret?: string | null;
};



export type HTTPValidationError = {
	detail?: Array<ValidationError>;
};



export type Message = {
	message: string;
};



export type MovieCreateIn = {
	title: string;
	year: string;
	rated?: string | null;
	released?: string | null;
	runtime?: string | null;
	genre?: string | null;
	director?: string | null;
	writer?: string | null;
	actors?: string | null;
	plot?: string | null;
	language?: string | null;
	country?: string | null;
	awards?: string | null;
	poster?: string | null;
	imdb_rating?: string | null;
	imdb_votes?: string | null;
	imdb_id: string;
	metascore?: string | null;
	box_office?: string | null;
	production?: string | null;
	website?: string | null;
};



export type MoviePublicOut = {
	title: string;
	year: string;
	rated?: string | null;
	released?: string | null;
	runtime?: string | null;
	genre?: string | null;
	director?: string | null;
	writer?: string | null;
	actors?: string | null;
	plot?: string | null;
	language?: string | null;
	country?: string | null;
	awards?: string | null;
	poster?: string | null;
	imdb_rating?: string | null;
	imdb_votes?: string | null;
	imdb_id: string;
	metascore?: string | null;
	box_office?: string | null;
	production?: string | null;
	website?: string | null;
	id: number;
	owner_id: number;
};



export type MovieUpdateIn = {
	title?: string | null;
	year: string;
	rated?: string | null;
	released?: string | null;
	runtime?: string | null;
	genre?: string | null;
	director?: string | null;
	writer?: string | null;
	actors?: string | null;
	plot?: string | null;
	language?: string | null;
	country?: string | null;
	awards?: string | null;
	poster?: string | null;
	imdb_rating?: string | null;
	imdb_votes?: string | null;
	imdb_id: string;
	metascore?: string | null;
	box_office?: string | null;
	production?: string | null;
	website?: string | null;
};



export type MoviesPublicOut = {
	data: Array<MoviePublicOut>;
	count: number;
};



export type NewPassword = {
	token: string;
	new_password: string;
};



export type Token = {
	access_token: string;
	token_type?: string;
};



export type UpdatePassword = {
	current_password: string;
	new_password: string;
};



export type UserCreate = {
	email: string;
	is_active?: boolean;
	is_superuser?: boolean;
	full_name?: string | null;
	password: string;
};



export type UserMovieCreateIn = {
	movies?: Array<number>;
};



export type UserMoviePublicOut = {
	movies?: Array<number>;
	owner_id: number;
};



export type UserMovieUpdateIn = {
	movies?: Array<number>;
};



export type UserPublic = {
	email: string;
	is_active?: boolean;
	is_superuser?: boolean;
	full_name?: string | null;
	id: number;
};



export type UserRegister = {
	email: string;
	password: string;
	full_name?: string | null;
};



export type UserUpdate = {
	email?: string | null;
	is_active?: boolean;
	is_superuser?: boolean;
	full_name?: string | null;
	password?: string | null;
};



export type UserUpdateMe = {
	full_name?: string | null;
	email?: string | null;
};



export type UsersPublic = {
	data: Array<UserPublic>;
	count: number;
};



export type ValidationError = {
	loc: Array<string | number>;
	msg: string;
	type: string;
};

