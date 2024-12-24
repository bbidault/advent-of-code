// https://adventofcode.com/2024/day/5

#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/topological_sort.hpp>
#include <fstream>
#include <vector>

/**
 * @brief Get the given manual pages sorted in topological order using the given tree definition
 *
 * @param aTreeEdges the edges of the tree of pages
 * @param aManualPages the manual pages to sort
 * @return std::vector<int> The given manual pages sorted in topological order
 */
std::vector<int> getTopologicalPages( std::vector<std::pair<int, int> > aTreeEdges, std::vector<int> aManualPages )
{
   // generate the tree that applies to this manual
   boost::adjacency_list<boost::vecS, boost::vecS, boost::directedS> graph;
   for ( int i = 0; i < aTreeEdges.size(); i++ )
   {
      if ( ( std::find( aManualPages.begin(), aManualPages.end(), aTreeEdges[i].first ) != aManualPages.end() ) &&
           ( std::find( aManualPages.begin(), aManualPages.end(), aTreeEdges[i].second ) != aManualPages.end() ) )
      {
         // we insert target to source because the back_inserter later will reverse the topological order
         boost::add_edge( aTreeEdges[i].second, aTreeEdges[i].first, graph );
      }
   }

   // sort the tree
   std::vector<int> sortedPages;
   topological_sort( graph, std::back_inserter( sortedPages ) );

   // remove the tree nodes that are not manual pages
   std::vector<int> sortedManualPages;
   for ( int i = 0; i < sortedPages.size(); i++ )
   {
      if ( std::find( aManualPages.begin(), aManualPages.end(), sortedPages[i] ) != aManualPages.end() )
      {
         sortedManualPages.push_back( sortedPages[i] );
      }
   }
   return sortedManualPages;
}

/**
 * @brief For part 1, sum the mid page numbers of valid manuals (pages meet topological order defined by the given tree).
 *        For part 2, sum the mid page numbers of invalid manuals.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return int the sum of the mid page numbers of the valid manual for part 1 and invalid ones for part 2
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   int sum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      bool ingestTree = true;
      std::vector<std::pair<int, int> > treeEdges;

      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         if ( line == "" ) // line break between the tree definition and the manuals
         {
            ingestTree = false;
         }
         else if ( ingestTree )
         {
            int source = std::stoi( line.substr( 0, 2 ) );
            int target = std::stoi( line.substr( 3, 2 ) );
            treeEdges.push_back( std::pair<int, int>( source, target ) );
         }
         else
         {
            // ingest the manual pages
            std::vector<int>  pages;
            std::stringstream ss( line );
            std::string page = "";
            while ( std::getline( ss, page, ',' ) )
            {
               pages.push_back( stoi( page ) );
            }

            // get the pages ordered topologicaly
            std::vector<int> sortedPages = getTopologicalPages( treeEdges, pages );
            // since each page appears at the most once per manual, comparing the given pages to the
            // sorted pages tells us if the manual is valid / meets topological order
            bool manualIsValid = ( pages == sortedPages );

            // sum the mid page number of the valid manual for part 1 and invalid ones for part 2
            if ( aPart1 && manualIsValid )
            {
               sum += pages[pages.size() / 2];
            }
            else if ( ( false == aPart1 ) && ( false == manualIsValid ) )
            {
               sum += sortedPages[sortedPages.size() / 2];
            }
            else
            {
               // do nothing
            }
         }
      }
      inputFile.close();
   }
   return sum;
}

/**
 * @brief Main function
 *
 * @param argc number of argument(s)
 * @param argv the argument(s)
 * @return int exit code
 */
int main( int argc, char *argv[] )
{
   if ( argc == 2 )
   {
      printf( "Part 1 solution: %d\n", compute( argv[1], true ) );
      printf( "Part 2 solution: %d\n", compute( argv[1], false ) );
   }
   return 0;
}
