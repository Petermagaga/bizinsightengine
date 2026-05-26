import API from "./axios";

export const getDashboard =
  async (datasetId) => {

    const response =
      await API.get(
        `/v1/insights/dashboard/${datasetId}/`
      );

    return response.data;
};