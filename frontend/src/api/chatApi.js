import API from "./axios";

export const askDatasetQuestion =
  async (
    datasetId,
    question
  ) => {

    const response =
      await API.post(
        `/v1/chat/${datasetId}/`,
        {
          question
        }
      );

    return response.data;
};

export const getChatHistory =
  async (datasetId) => {

    const response =
      await API.get(
        `/v1/chat/history/${datasetId}/`
      );

    return response.data;
};