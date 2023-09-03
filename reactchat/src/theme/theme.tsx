import {createTheme, responsiveFontSizes} from "@mui/material";

// build our own theme
declare module "@mui/material/styles" {
    interface Theme {
        primaryAppBar: {
            height: number;
        };
        primaryDraw: {
            width: number;
            closed: number;
        };
    }

    // allows us to utilize the new primaryAppBar property inside the new theme we created above
    interface ThemeOptions {
        primaryAppBar: {
            height: number;
        };

        primaryDraw: {
            width: number;
            closed: number;

        };
    }
}

//customize our theme
export const createMuiTheme = () => {
    let theme = createTheme({

        typography: {
            fontFamily: ['IBM Plex Sans', "sans-serif"].join(","),
        },

        primaryAppBar: {
            height: 60,
        },

        primaryDraw: {
            width: 240,
            closed: 70,
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
    theme = responsiveFontSizes(theme);
    return theme;
}

export default createMuiTheme;