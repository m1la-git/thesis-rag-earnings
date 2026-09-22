%%
% TUM Corporate Design Book
% Michael Riesch (michael.riesch@tum.de) adapted by Lukas Heidegger (lukas.heidegger@tum.de)
% Based on the templates from https://www.tum.de/cd
%
% Template for scientific theses, lecture notes, ...
%
%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tum-book}[2018/10/08 TUM Corporate Design Book v0.3]

% process options
\DeclareOption{a4paper}{%
  \PassOptionsToPackage{a4paper}{tum-base-text}
  % 12pt, NOT the template's 13pt. Changed 2026-09-12 on Kamila's ruling:
  % the chair's written guidelines say "Font Size: 12" (the
  % formatting table and section 6), and where the chair's own template
  % disagrees with the chair's own text, the text governs. This is a
  % deliberate divergence from the TUM template, not a stale value: if this
  % file is ever re-downloaded from the corporate-design source it will come
  % back as 13pt and must be changed again. The alternative -- passing
  % fontsize=12pt from main.tex -- was not used: it would win only by option
  % ordering, which is not something a reader can check from the document.
  \PassOptionsToClass{a4paper,fontsize=12pt}{scrbook}
}
\DeclareOption{a5paper}{%
  \PassOptionsToPackage{a5paper}{tum-base-text}
  \PassOptionsToClass{a5paper,fontsize=12pt}{scrbook}
}
\DeclareOption{twoside}{\PassOptionsToClass{twoside}{scrbook}}
\DeclareOption{oneside}{\PassOptionsToClass{oneside}{scrbook}}
\DeclareOption{times}{\PassOptionsToPackage{times}{tum-base}}
\DeclareOption{german}{%
  \PassOptionsToPackage{german}{tum-base}
  \PassOptionsToPackage{german}{nomencl}
}
\DeclareOption{english}{%
  \PassOptionsToPackage{english}{tum-base}
  \PassOptionsToPackage{english}{nomencl}
}
\ExecuteOptions{twoside,a4paper}
\ProcessOptions\relax

% load base class
\LoadClass[pagesize,bibtotoc,idxtotoc,numbers=noenddot]{scrbook}

% load TUM base packages
\RequirePackage{tum-base}
\RequirePackage{tum-base-text}

\newcommand{\thepublisher}{~}
\newcommand{\publisher}[1]{\renewcommand{\thepublisher}{#1}}
\newcommand{\thetitledescription}{~}
\newcommand{\titledescription}[1]{\renewcommand{\thetitledescription}{#1}}
\newcommand{\thefineprint}{~}
\newcommand{\fineprint}[1]{\renewcommand{\thefineprint}{#1}}

% custom titlepage
\AtBeginDocument{
    \begin{titlepage}
    \thispagestyle{titlepage}
    \ifavier
    % title page a4
    \begin{singlespace}
    \vbox{}

    \fontfamily{phv}\selectfont
    {~\\}
    { \flushleft\LARGE\bfseries\@title\par }
    { \flushleft\Large\@subtitle\par }

    { \flushleft\large\textcolor{TUMBlau}{\textbf{\@author}}\par }
    \vspace{1cm}
    { \flushleft\large\thetitledescription\par}
    \vspace{1cm}
    { \flushleft\normalsize\thefineprint\par }

    \begin{textblock*}{13cm}[1,1](\paperwidth-2\tumlogoheight,
      \paperheight-1\tumlogoheight)
      \raggedleft
      \includegraphics[width=11cm]{tum-resources/images/TUM_Uhrenturm.png}\par
    \end{textblock*}
    \end{singlespace}

    \else
    % title page a5
    \fontfamily{phv}\selectfont
    \vspace{12pt}
    { \flushleft\huge\bfseries\@title\par }
    { \flushleft\Large\@subtitle\par }
    \vspace{12pt}
    { \flushleft\Large\textcolor{TUMBlau}{\textbf{\@author}}\par
      \thepublisher\par }
    { \flushleft\large\thetitledescription\par }
    { \flushleft\normalsize\thefineprint\par }

    \begin{textblock*}{8cm}[1,1](\paperwidth-2\tumlogoheight, \paperheight)
      \raggedleft
      \includegraphics[width=8cm]{tum-resources/images/TUM_Uhrenturm.png}\par
    \end{textblock*}


    \fi

    \vfill
  \end{titlepage}
}

% custom header/footer
\RequirePackage{fancyhdr}
\fancypagestyle{plain}{
  % clear everything
  \fancyhead{}
  \fancyfoot{}

  % page numbers
  \fancyhead[R]{\thepage}
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0pt}
}

\fancypagestyle{titlepage}{%
  % clear everything
  \fancyhead{}
  \fancyfoot{}
 
  % threeliner
  \fancyhead[L]{%
    \vbox to \tumlogoheight{%
    \vspace{1cm}
      \fontfamily{phv}\fontsize{9}{11}\selectfont\textcolor{TUMBlau}{%
        \thegroup\\
        \thedepartment\\
        \theuniversity
      }
    }
  }

  % logo
  \fancyhead[R]{%
    \vbox to \tumlogoheight{%
    \vspace{1cm}
      \includegraphics[height=\tumlogoheight]%
                      {tum-resources/images/Universitaet_Logo_RGB.pdf}\ \ \
    }
  }
}

\pagestyle{plain}

\newcommand{\printthesisdisclaimer}[2]{%
\newpage
  \pagestyle{empty}
  {
    \fontfamily{times}\selectfont
    \noindent
    { \flushleft\huge\bfseries\center Declaration of Academic Integrity \par}
    \vspace{10mm}
    \noindent 
I hereby declare that the thesis submitted is my own unaided work. All direct or indirect sources used are acknowledged as references.
\par\noindent
I am aware that the thesis in digital form can be examined for the use of unauthorized aid and in order to determine whether the thesis as a whole or parts incorporated in it may be deemed as plagiarism. For the comparison of my work with existing sources I agree that it shall be entered in a database where it shall also remain after examination, to enable comparison with future theses submitted. Further rights of reproduction and usage, however, are not granted here.
\par\noindent
This paper was not previously presented to another examination board and has not been published. \par
\begin{center}
        \vspace{30mm}\noindent
    #1 \hspace{5cm} #2\par
\end{center}


  }
  \newpage
  \pagestyle{plain}
}

\newcommand{\printdedication}[1]{%
  \thispagestyle{empty}
  \phantom{u}
  \phantom{1}\vspace{6cm}
  \begin{center}
    \fontfamily{times}\selectfont
    #1
  \end{center}
  \newpage
  \pagestyle{plain}
}

\newcommand{\printphdthesistitle}[5]{%
  \pagestyle{empty}
  \cleardoublepage
  \pagestyle{titlepage}
  \begin{otherlanguage}{ngerman}
    { \flushleft\fontfamily{times}\selectfont\large\thedepartment\par
      \thegroup\par
    }
    \vspace{12pt}
    { \flushleft\fontfamily{times}\selectfont\huge\bfseries\@title\par }
    { \flushleft\flushleft\fontfamily{times}\Large
      \textcolor{TUMBlau}{\textbf{\@author}}\par}
    { \flushleft\fontfamily{times}\selectfont\normalsize
      Vollständiger Abdruck der von der \thedepartment{} der
      \theuniversity{} zur Erlangung des akademischen Grades eines\\
      \textbf{Doktor-Ingenieurs (Dr.-Ing.)}\\
      genehmigten Dissertation.\par
    }
    { \flushleft\fontfamily{times}\selectfont\normalsize
      Vorsitzende(r): #3\par
      Prüfer der Dissertation:
      \begin{enumerate}[nolistsep]
      \item #4
      \item #5
      \end{enumerate}
    }
    \vspace{12pt}
    { \flushleft\fontfamily{times}\selectfont\normalsize
      Die Dissertation wurde am #1 bei der \theuniversity{} eingereicht und
      durch die \thedepartment{} am #2 angenommen.\par}
  \end{otherlanguage}
  \newpage
  \pagestyle{plain}
}

%quotation
\def\signed #1{{\leavevmode\unskip\nobreak\hfil\penalty50\hskip2em
  \hbox{}\nobreak\hfil(#1)%
  \parfillskip=0pt \finalhyphendemerits=0 \endgraf}}

\newsavebox\mybox
\newenvironment{aquote}[1]
  {\savebox\mybox{#1}\begin{quote}}
  {\signed{\usebox\mybox}\end{quote}}
  
  
\usepackage{chngcntr}
\counterwithout{footnote}{chapter}
% Line spacing 2.0 as Word renders it, which is what the chair's guideline
% ("line spacing of 2.0") refers to. Word's single spacing for Times New Roman
% 12 pt is 13.8 pt, so its double is 27.6 pt. LaTeX's single spacing at 12 pt is
% 14.5 pt, so the stretch is 2 x 13.8 / 14.5 = 1.9035. setspace's
% [doublespacing] option would give only about 24 pt (twice the font size,
% not Word's 2.0). Floats and footnotes stay single-spaced under setspace.
\usepackage{setspace}
\setstretch{1.9035}
\makeatletter
\makeatother
\usepackage{enumitem}
\setlist{nosep}
\renewcommand*{\chapterheadstartvskip}{\vspace*{0cm}}
\renewcommand*{\chapterheadendvskip}{\vspace{0cm}}

% Distance between paragraphs: none. APA 7 marks a paragraph by its first-line
% indent (\parindent below) and adds no space between paragraphs; the template's
% 15pt skip was removed for that reason. Stretch is zero too, so page breaks
% cannot reintroduce it.
\setlength{\parskip}{0pt plus 0pt}

\usepackage{url}
\usepackage{hyperref}
\usepackage{csquotes}

\setcounter{secnumdepth}{-1}



\SetBlockThreshold{0}

\parindent=1.27cm
\newcommand{\periodafter}[1]{#1.~~}
\usepackage{titlesec}
\titleclass{\chapter}{straight}
\titleformat{\chapter}{\normalfont\normalsize\bfseries\centering}{}{1em}{}
% Section and subsection headings take no extra space at all: APA adds no blank
% line above or below a heading, the surrounding double spacing carrying the
% separation by itself. 1sp rather than 0pt, so the skip stays positive -- a
% non-positive beforeskip suppresses the first-line indent of the paragraph
% that follows, and APA wants it indented. The chapter keeps 18pt/6pt because
% \titleclass makes it a straight, non-page-breaking heading, so it has to
% separate itself from the text above it. No stretch, so page breaks cannot
% enlarge any of them, and \parskip stays 0. Typography (bold, italic, centring,
% levels) is unchanged. The former -12pt after-skips offset a 15pt \parskip and
% must not return without it.
\titlespacing{\chapter}{0pt}{18pt}{6pt}
\titleformat{\section}{\normalfont\normalsize\bfseries}{}{1em}{}
\titlespacing{\section}{0pt}{1sp}{1sp}
\titleformat{\subsection}{\normalfont\normalsize\bfseries\itshape}{}{1em}{}
\titlespacing{\subsection}{0pt}{1sp}{1sp}
\titleformat{\subsubsection}[runin]{\normalfont\normalsize\bfseries}{}{1em}{\periodafter}
\titlespacing{\subsubsection}{1.27cm}{0pt}{0pt}

% A block quotation is double-spaced like the body and carries no extra space
% above or below it. csquotes' block threshold is 0, so \enquote{} lands in this
% same environment.
\usepackage{etoolbox}
\AtBeginEnvironment{quote}{\setlength{\topsep}{0pt}\setlength{\partopsep}{0pt}}

%% Control the fonts and formatting used in the table of contents.

\usepackage[titles]{tocloft}

%% Aesthetic spacing redefines that look nicer to me than the defaults.

\setlength{\cftbeforechapskip}{2ex}
\setlength{\cftbeforesecskip}{0.5ex}

\renewcommand{\cftchapfont}{\bfseries}

\usepackage[labelfont=bf,textfont=it,singlelinecheck=off,justification=raggedright]{caption}
\renewcommand{\thefigure}{\arabic{figure}}
\renewcommand{\thetable}{\arabic{table}}
\setlength{\abovecaptionskip}{15pt plus 3pt minus 2pt}
\setlength{\belowcaptionskip}{15pt plus 3pt minus 2pt}
\captionsetup[figure]{labelsep=newline}
\captionsetup[table]{labelsep=newline}

\usepackage[capposition=top]{floatrow}



\usepackage{graphicx}
\usepackage{verbatim}
\graphicspath{{img/}}
\usepackage{wrapfig}
\usepackage[backend=biber,style=apa, pagetracker=true]{biblatex}
\addbibresource{literature.bib}
\DeclareLanguageMapping{english}{english-apa}
\pdfimageresolution 300

\newcommand{\paragraphWithHeading}[1]{\paragraph{#1}\mbox{}\newline}
\pgfplotsset{compat=1.15}