import API
 from "./authApi";


 
export const getDashboard =
  async (datasetId) => {

    const response =
      await API.get(
        `insights/dashboard/${datasetId}/`
      );

    return response.data;
};