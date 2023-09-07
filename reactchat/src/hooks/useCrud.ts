import useAxiosWithInterceptor from "../helpers/jwtinterceptor";
import { BASE_URL } from "../config"
import { useEffect, useState } from 'react'

// CREATE RETURN/READ UPDATE DELETE
// declared an interaface that has generic type T
// the interface defines 4 paremeters
interface IuseCrud<T> {
    dataCRUD: T[];
    // function returning a promise without a value
    fetchData: () => Promise<void>;
    error: Error | null;
    isLoading: boolean;
}

// create a React hook to provide all the centralized functionality to perform the CRUD operations on our backend API
// hook is a special function that allows us to add state and other React features to functional components -- sort of like a class
// a way of reusing stateful logic w/o the need for class components. Ex built-in hooks : useState(), useEffect(), etc.
// this React hook/function has 2 parameters: initalData of type T[] and apiURL of type String
const useCrud = <T>(initalData: T[], apiURL: string): IuseCrud<T> => {
    const jwtAxios = useAxiosWithInterceptor();
    // create a new state, initial state is empty
    const [dataCRUD, setDataCRUD] = useState<T[]>(initalData)
    // create a new state to store the error
    const [error, setError] = useState<Error | null>(null)
    const [isLoading, setIsLoading] = useState(false)
 
    // building a function to fetch data from the API
    const fetchData = async () => {
        setIsLoading(true)
        try{
            // build an Axios request to the API Server through the interceptor, await the return of that information
            const response = await jwtAxios.get(`${BASE_URL}${apiURL}`, {})
            // while that happens, the rest of the code gets run
            const data = response.data
            //load up the data here
            setDataCRUD(data)
            setError(null)
            setIsLoading(false)
            return data;
        } catch (error: any){
            if (error.response && error.response.status === 400) {
                setError(new Error("400"))
            }
            setIsLoading(false)
            throw error;
        }
    };

    // return back to the components so it can be utilized when a component utilizes our custom React hook
    return {fetchData, dataCRUD, error, isLoading}
}
export default useCrud;