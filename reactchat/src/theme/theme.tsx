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
        secondaryDraw: {
            width: number;
        }
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

        secondaryDraw: {
            width: number;
        }
    }
}

//customize our theme
export const createMuiTheme = (mode: "light" | "dark") => {
    let theme = createTheme({

        typography: {
            fontFamily: ['IBM Plex Sans', "sans-serif"].join(","),
            body1: {
                fontWeight: 500,
                letterSpacing: "-0.5px",
    
            },
            body2: {
                fontWeight: 500,
                fontSize: "15px",
                letterSpacing: "-0.5px",

            },
        },

        primaryAppBar: {
            height: 60,
        },

        primaryDraw: {
            width: 240,
            closed: 70,
        },

        secondaryDraw: {
            width: 240,
        },
        
        palette: {
            mode,
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