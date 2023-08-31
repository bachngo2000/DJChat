import {createTheme} from "@mui/material";

// build our own theme
declare module "@mui/material/styles" {
    interface Theme {
        primaryAppBar: {
            height: number;
        };
    }

    // allows us to utilize the new primaryAppBar property inside the new theme we created above
    interface ThemeOptions {
        primaryAppBar: {
            height: number;
        };
    }
}

//customize our theme
export const createMuiTheme = () => {
    const theme = createTheme({

        typography: {
            fontFamily: ['IBM Plex Sans', "sans-serif"].join(","),
        },

        primaryAppBar: {
            height: 60,
        },

        components: {
            MuiAppBar: {
                defaultProps: {
                    color: "default",
                    elevation: 0,
                }
            }
        }
    });
    return theme;
}

export default createMuiTheme;