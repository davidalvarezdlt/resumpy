% Basic class creation
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{sitges}

%\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
%\ProcessOptions \relax
\LoadClass{report}

% Include Packages
\RequirePackage[a4paper, margin=1cm, right=1cm, footskip=1.5cm, bottom=2.5cm]{geometry}
\RequirePackage{fontawesome}
\RequirePackage[hidelinks]{hyperref}
\RequirePackage[sfdefault]{roboto}
%\RequirePackage[default,osfigures,scale=0.95]{opensans}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{xcolor}
\RequirePackage{fancyhdr}
\RequirePackage{progressbar}
\RequirePackage{paracol}
%\RequirePackage[demo]{graphicx}

\usepackage{setspace}
\RequirePackage{enumitem}
\setlist[itemize]{leftmargin=*}

% Define Header Variables
\newcommand{\name}[1]{\newcommand{\@name}{#1}}
\newcommand{\profession}[1]{\newcommand{\@profession}{#1}}
\newcommand{\email}[1]{\newcommand{\@email}{#1}}
\newcommand{\scholar}[2]{\newcommand{\@scholarurl}{#1}\newcommand{\@scholarlabel}{#2}}
\newcommand{\github}[2]{\newcommand{\@githuburl}{#1}\newcommand{\@githublabel}{#2}}
\newcommand{\linkedin}[2]{\newcommand{\@linkedinurl}{#1}\newcommand{\@linkedinlabel}{#2}}
\newcommand{\twitter}[2]{\newcommand{\@twitterurl}{#1}\newcommand{\@twitterlabel}{#2}}
\newcommand{\website}[2]{\newcommand{\@websiteurl}{#1}\newcommand{\@websitelabel}{#2}}
\newcommand{\location}[1]{\newcommand{\@location}{#1}}

% Define theme colors
\definecolor{bg_color}{rgb}{0.95,0.95,0.95}
\definecolor{accent_color}{rgb}{0.5,0.5,0.5}
\definecolor{title_color}{rgb}{0.80,0.80,0.80}
\definecolor{blue_color}{HTML}{027bbb}

% HEADER COMMANDS
\pagestyle{fancy}
\fancyfoot[CE,CO]{
{\faGoogle\hspace{3pt}\texttt{\href{\@scholarurl}{\@scholarlabel}}}
\hspace{5pt}|\hspace{5pt}
{\faGithub\hspace{3pt}\texttt{\href{\@githuburl}{\@githublabel}}}
\hspace{5pt}|\hspace{5pt}
{\faLinkedin\hspace{3pt}\texttt{\href{\@linkedinurl}{\@linkedinlabel}}}
\hspace{5pt}|\hspace{5pt}
{\faTwitter\hspace{3pt}\texttt{\href{\@twitterurl}{\@twitterlabel}}}
\hspace{5pt}|\hspace{5pt}
{\faLink\hspace{3pt}\texttt{\href{\@websiteurl}{\@websitelabel}}}
}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\setlength{\parindent}{0pt}

% LAST UPDATE
\newcommand{\lastupdate}[1]{
    {\footnotesize\color{accent_color}#1}
}

% HEADER COMMANDS
\newcommand{\cvheader}[1]{
    {\Huge\bfseries\@name}
    \par\smallskip
    {\large\color{accent_color}\@profession\par}
    %\vspace{0.4cm}
\par
}

% SECTIONS COMMANDS
\newcommand{\cvsection}[1]{
\par \medskip
{\noindent\Large\color{blue_color}{#1}\par}
\medskip
}

% SECTIONS COMMANDS
\newcommand{\cvsidebarsection}[1]{
\par \bigskip
{\noindent\bfseries{#1}\par}
\medskip
}

% SIDEBAR SPECIFIC COMMANDS
\newcommand{\detailitem}[3]{
{\small \textbf{#2} \par #3 \par} \medskip}

\newcommand{\languageitem}[3]{
{\par\footnotesize #1 (#2) \par}
\progressbar[width=0.20\textwidth, roundnessr=0, ticksheight=0pt, heightr=0.5, borderwidth=0pt, emptycolor=bg_color, filledcolor=accent_color]{#3}
}

\newcommand{\skillitem}[1]{
\tikz[baseline]\node[anchor=base,draw=black!30,inner xsep=1ex,inner ysep =0.75ex,text height=1.5ex,text depth=.25ex]{#1};
}

\newcommand{\skillset}[2]{
{\small #1}
\par
\smallskip
{\footnotesize\color{accent_color}#2}
\par
}

\newcommand{\courseitem}[3]{
#1
\par
{\footnotesize #2 - \texttt{#3}}
\par
}

% PROJECTS SECTION
\newcommand{\projectitem}[3]{
\par
#1
\par
{\footnotesize\color{accent_color} #2}
\par
\smallskip
{\footnotesize #3}
}

% WORK EXPERIENCE SECTION
\newenvironment{experienceitem}[3]{
{\par \noindent\bfseries #1 @ #2}
\par
{\noindent\footnotesize\color{accent_color} #3}
\par \medskip
\footnotesize
}{}

% EDUCATION EXPERIENCE SECTION
\newenvironment{educationitem}[4]{
\par
{\small{#1 \hfill {\footnotesize }}}
{\footnotesize\color{accent_color} {#2}}
\par
{\noindent\bfseries #3}
\par
\def\temp{#4}\ifx\temp\empty\else
{\footnotesize\color{accent_color}#4}
\fi
\par \medskip
\footnotesize
}{}

% AWARDS SECTION
\newenvironment{awarditem}[2]{
\par
\textbf{#1}
\par
{\footnotesize\color{accent_color} #2}
\par \smallskip \footnotesize
}{\normalsize}

% PUBLICATIONS SECTION
\newenvironment{publicationitem}[4]{
\par
{\footnotesize\color{accent_color} #2 - #3}
\par
\textbf{#1}
\par
{\footnotesize\color{accent_color} #4}
\par \medskip \footnotesize
}{}

% FACTS ITEM
\newcommand{\factitem}[1]{
\par
{\footnotesize #1}
\par
}
