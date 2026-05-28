import API from "./axios";
export const getDatasets =
  async () => {

    const response =
      await API.get(
        "/data/datasets/"
      );

    return response.data;
  };


  