import {Gamer, Word} from "./types.ts";
import WordleGameCard from "./WordleGameCard.tsx";
import './App.css'


export default function App() {
    const gamer : Gamer = {
        id : "xx00",
        name: "alligator",
        score : 230,
        password : "helloworld",
    };

    const word : Word = {
        id : "xxx1",
        chaine : "MESMER",
        len : 6,
        definition : "Hypnotysm pioner Franz"
    }

    return (
        <>
            <h1>
                Trouve le Mot
            </h1>
            <div className="main-container">
                <WordleGameCard user={gamer} find_word={word} />
            </div>
        </>
    )
}