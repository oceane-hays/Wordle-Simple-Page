export interface Word {
    id: string
    chaine: string
    definition : string
}

export interface Gamer {
    id: string
    name: string
    score: number
    password : string
}

export interface WordleGameCardProps {
    user : Gamer,
    find_word : Word,
}