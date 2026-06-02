import {
  useEffect,
  useState
} from "react";

import {
  askDatasetQuestion,
  getChatHistory
} from "../api/chatApi";

function DatasetChat({
  datasetId
}) {

  const [question, setQuestion] =
    useState("");

  const [messages, setMessages] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  useEffect(() => {

    if (!datasetId) return;

    loadHistory();

  }, [datasetId]);

  const loadHistory =
    async () => {

    try {

      const history =
        await getChatHistory(
          datasetId
        );

      const transformed = [];

      history.forEach(chat => {

        transformed.push({
          role: "user",
          content: chat.question
        });

        transformed.push({
          role: "assistant",
          content: chat.answer,
          source: chat.source
        });

      });

      setMessages(
        transformed
      );

    } catch (error) {

      console.error(error);
    }
  };

  const handleAsk =
    async () => {

    if (!question.trim())
      return;

    const currentQuestion =
      question;

    setQuestion("");

    setMessages(prev => [
      ...prev,
      {
        role: "user",
        content:
          currentQuestion
      }
    ]);

    setLoading(true);

    try {

      const response =
        await askDatasetQuestion(
          datasetId,
          currentQuestion
        );

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content:
            response.answer,
          source:
            response.source
        }
      ]);

    } catch (error) {

      console.error(error);

      setMessages(prev => [
        ...prev,
        {
          role: "assistant",
          content:
            "Failed to get response."
        }
      ]);

    } finally {

      setLoading(false);
    }
  };

  return (

    <div
      style={{
        marginTop: "40px",
        background: "white",
        padding: "20px",
        borderRadius: "12px"
      }}
    >

      <h2>
        Ask Your Data
      </h2>

      <div
        style={{
          maxHeight: "400px",
          overflowY: "auto",
          marginBottom: "20px"
        }}
      >

        {messages.map(
          (message, index) => (

          <div
            key={index}
            style={{
              marginBottom: "16px"
            }}
          >

            <strong>

              {message.role ===
              "user"
                ? "You"
                : "AI"}

              :

            </strong>

            <div>
              {
                message.content
              }
            </div>

            {message.source && (

              <small>

                Source:
                {" "}
                {
                  message.source
                }

              </small>

            )}

          </div>

        ))}

        {loading && (

          <div>

            AI is analyzing
            your dataset...

          </div>

        )}

      </div>

      <textarea
        value={question}
        onChange={(e) =>
          setQuestion(
            e.target.value
          )
        }
        rows={3}
        placeholder="Ask a question about your dataset..."
        style={{
          width: "100%",
          padding: "12px"
        }}
      />

      <button
        onClick={handleAsk}
        disabled={loading}
        style={{
          marginTop: "10px",
          padding:
            "10px 20px"
        }}
      >
        Ask AI
      </button>

    </div>
  );
}

export default DatasetChat;