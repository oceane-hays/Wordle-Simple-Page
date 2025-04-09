import {useEffect, useState} from 'react'
import {Word, WordleGameCardProps} from "./types.ts";
import "./GameCard.css"
import trophee from "./assets/trophee.png"
import userIcon from "./assets/user.png"
import clockIcon from "./assets/clock.png"
import lightIcon from "./assets/lightIcon.png"

export default function WordleGameCard({ user, find_word }: WordleGameCardProps) {
    const [timeLeft, setTimeLeft] = useState(60)
    const [score, setScore] = useState(find_word.chaine.length * 10) // Le joueur part avec un score de 10 ∗ len(m)
    const [currentQuestion] = useState({
        text: find_word.definition,
        nb_lettre: find_word.chaine.length,
        completedSegments: 1,
    })

    const [suggIsActive, setSuggIsActive] = useState(false)
    const [suggestions, setSuggestions] = useState<string[]>([])

    useEffect(() => {
        if (timeLeft <= 0) return

        const timer = setTimeout(() => {
            setTimeLeft(timeLeft - 1)
        }, 1000)

        return () => clearTimeout(timer)
    }, [timeLeft])

    // Calculate le progress percentage
    const progressPercentage = (timeLeft / 60) * 100

    const findSuggestion = (word : Word) : String[] => {
        const sugg : String[] = ["DEIMOS", "MESMER", "SLIMES"];

        return sugg
    }

    return (
       <>
          <div className="card-container">
              {/* User profile and score */}
              <div className="profile">
                  <div className="user-profile">
                      <div className="avatar">
                          <img width="100" height="100" src={userIcon} alt="user"/>
                      </div>
                      <span className="username">alligator</span>
                  </div>

                  <div className="score-container">
                      <div className="trophy-icon">
                          <img src={trophee} width={40} height={40} alt="Trophee"/>
                      </div>
                      <span className="score">{score}</span>
                  </div>

                  {/* Time progress bar */}
                  <div className="progress-bar-container">
                      <div className="progress-bar-behind">
                          <div className="progress-bar" style={{width: `${progressPercentage}%`}}/>
                      </div>
                      <div className="time-remaining">{timeLeft}</div>
                  </div>

              </div>

              <div className="game">
                  {/* Question and progress */}
                  <div className="question-section">
                      <h2 className="question-text">{currentQuestion.text}</h2>
                          <div className="segment-container">
                              {Array.from({length: currentQuestion.nb_lettre}).map((_, index) => (
                                  <>
                                      <div
                                          key={index}
                                          className={`segment ${index < currentQuestion.completedSegments ? "segment-completed" : ""}`}
                                      >
                                          _
                                      </div>
                                  </>

                              ))}
                          </div>
                  </div>

                  {/* Timer */}
                  <div className="timer-section">
                      <div className="clock-icon">
                          <img src={clockIcon} width={80} height={80} alt="clock-icon"/>
                      </div>
                      <div className="time-display">{timeLeft}</div>
                      {
                          timeLeft <= 50 ? <img src={lightIcon} width={70} height={70} onClick={() => {
                              setScore(score - 20); // le user perd 20 points s'il decouvrent les suggestions
                              setSuggIsActive(true)
                            }}/>

                          : <></> // rien du tout
                      }
                  </div>
              </div>

              {/* Suggestion Container */}
              { suggIsActive && (
                  <div className="suggestion-container">
                      <h3>suggestion</h3>
                      <div className="suggestion">
                          {
                              suggestions.map((word, index) => (
                                  <div key={index} className="suggestion-item">
                                      {word}
                                  </div>
                              ))
                          }
                      </div>
                  </div>
              )}
          </div>
       </>
    )
}

