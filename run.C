void run( TString scanchainname, const char* input_path, TString treename, TString output_path, TString nevents = "-1", TString compilerflag = "", TString opt = "" )
{

    // Load all *.so files in current directory
    TString analysis_base = gSystem->Getenv("ANALYSIS_BASE");
    if ( analysis_base.IsNull() )
        analysis_base = "./";
    std::cout << "Checking packages in the directory " << analysis_base << std::endl;
    TSystemDirectory dir( analysis_base, analysis_base );
    TList *files = dir.GetListOfFiles();

    if ( files )
    {
        TSystemFile *file;
        TString fname;
        TIter next( files );

        std::cout << "Adding shared object libraries" << std::endl;
        while ( ( file = ( TSystemFile* )next() ) )
        {
            fname = file->GetName();

            if ( file->IsDirectory() && ( fname.Contains( "CORE" ) || fname.EqualTo( "rooutil" ) ) )
            {
                if ( fname.EqualTo( "CORE" ) )
                {
                    TString sopath = analysis_base + "/" + fname + "/CMS3_" + fname + ".so";
                    std::cout << "Adding " << sopath  << std::endl;
                    gSystem->Load( sopath );
                }
                else
                {
                    TString sopath = analysis_base + "/" + fname + "/" + fname + ".so";
                    std::cout << "Adding " << sopath  << std::endl;
                    gSystem->Load( sopath );
                }
            }
        }
    }

    TString pwd = gSystem->WorkingDirectory();
    gROOT->ProcessLine( ".include " + analysis_base );
    gROOT->ProcessLine( ".L " + scanchainname + "+" + compilerflag );
    gROOT->ProcessLine( Form( "TString input_path = \"%s\";", input_path ) );
    gROOT->ProcessLine( "TString output_path = \"" + output_path + "\";" );
    gROOT->ProcessLine( "TString ttreename = \"" + treename + "\";" );
    gROOT->ProcessLine( "TString opt = \"" + opt + "\";" );
    gROOT->ProcessLine( "TChain *chain = new TChain(ttreename);" );
    gROOT->ProcessLine( "TObjArray* files = input_path.Tokenize(\",\");" );
    gROOT->ProcessLine( "for (unsigned int ifile = 0; ifile < files->GetEntries(); ++ifile) { TString filepath = ((TObjString*) files->At(ifile))->GetString(); std::cout << \"Adding to TChain: file = \" << filepath << std::endl; chain->Add(filepath); }" );
    gROOT->ProcessLine( "TString CMSxVersion = TString(gSystem->BaseName(gSystem->DirName(chain->GetListOfFiles()->At(0)->GetTitle())));");//.ReplaceAll(\"/\",\"_\").ReplaceAll(\"-\",\"_\");" );
    gROOT->ProcessLine( "TString sample_name = TString(gSystem->BaseName(gSystem->DirName(gSystem->DirName(chain->GetListOfFiles()->At(0)->GetTitle()))));");//.ReplaceAll(\"/\",\"_\").ReplaceAll(\"-\",\"_\");" );
    gROOT->ProcessLine( "TString file_name   = TString(gSystem->BaseName(gSystem->BaseName(chain->GetListOfFiles()->At(0)->GetTitle())));");//.ReplaceAll(\"/\",\"_\").ReplaceAll(\"-\",\"_\");" );
//    gROOT->ProcessLine( "TString sample_name_based_opt_string = sample_name + \"_\" + CMSxVersion + \"_\" + file_name;");//.ReplaceAll(\"/\",\"_\").ReplaceAll(\"-\",\"_\");" );
    gROOT->ProcessLine( "TString sample_name_based_opt_string = input_path + opt" );
    gROOT->ProcessLine( "std::cout << \"base_optstr = \" << sample_name_based_opt_string << std::endl;" );
    gROOT->ProcessLine( "std::cout << std::endl;" );
    gROOT->ProcessLine( "std::cout << std::endl;" );
    gROOT->ProcessLine( "std::cout << \"   .\" << std::endl;" );
    gROOT->ProcessLine( "std::cout << \"  ..: Start " + scanchainname + " ...\" << std::endl;" );
    gROOT->ProcessLine( "std::cout << std::endl;" );
    gROOT->ProcessLine( "std::cout << std::endl;" );
    gROOT->ProcessLine( "ScanChain(chain,output_path,sample_name_based_opt_string," + nevents + ");" );
    gROOT->ProcessLine( "std::cout << std::endl;" );
    gROOT->ProcessLine( "std::cout << std::endl;" );
    gROOT->ProcessLine( "std::cout << \"   .\" << std::endl;" );
    gROOT->ProcessLine( "std::cout << \"  ..: Finished " + scanchainname + " ...\" << std::endl;" );
    gROOT->ProcessLine( "std::cout << std::endl;" );
    gROOT->ProcessLine( "std::cout << std::endl;" );
    
}
