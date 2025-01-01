// https://adventofcode.com/2024/day/23

#include <algorithm>
#include <fstream>
#include <map>
#include <set>

/**
 * @brief Count the number of sub networks of three interconnected computers within the complete network.
 *
 * @param aConnections a map of computers and connected computers
 * @return int the number of sub networks of three interconnected computers within the complete network
 */
int getThreeComputerNetworksCount( std::map<std::string, std::set<std::string> > &aConnections )
{
   int count                                                             = 0;
   std::map<std::string, std::set<std::string> >::iterator computer1_itr = aConnections.begin();
   for (; computer1_itr != aConnections.end(); computer1_itr++ )
   {
      std::set<std::string>::iterator computer2_itr = computer1_itr->second.begin();
      for (; computer2_itr != computer1_itr->second.end(); computer2_itr++ )
      {
         // find the computers that are connected to both computer 1 and 2
         std::set<std::string> intersection;
         std::set_intersection( computer1_itr->second.begin(), computer1_itr->second.end(),
                                aConnections[*computer2_itr].begin(), aConnections[*computer2_itr].end(),
                                std::inserter( intersection, intersection.begin() ) );
         // one of the computers name needs to start with by the letter 't'
         if ( ( computer1_itr->first[0] == 't' ) || ( ( *computer2_itr )[0] == 't' ) )
         {
            count += intersection.size();
         }
         else
         {
            std::set<std::string>::iterator computer3_itr = intersection.begin();
            for (; computer3_itr != intersection.end(); computer3_itr++ )
            {
               if ( ( *computer3_itr )[0] == 't' )
               {
                  count++;
               }
            }
         }
      }
   }
   // each network is counted 6 time, once for each pair of computer 1 and 2 possible within a list of 3 computers
   return count / 6;
}

/**
 * @brief Recursive function. Find the largest sub network of interconnected computers.
 *
 * @param aComputers a set of candidate computers to be part of the network
 * @param aConnections a map of computers and connected computers
 * @param aCurrentNetwork the current network of connected computers
 * @return std::set<std::string> the largest sub network of interconnected computers
 */
std::set<std::string> getLargestNetwork( std::set<std::string>                         &aComputers,
                                         std::map<std::string, std::set<std::string> > &aConnections,
                                         std::set<std::string>                         &aCurrentNetwork )
{
   // the base largest set is the current set
   std::set<std::string> largestSet             = aCurrentNetwork;
   std::set<std::string>::iterator computer_itr = aComputers.begin();
   while ( computer_itr != aComputers.end() )
   {
      aCurrentNetwork.insert( *computer_itr ); // add another computer to the set
      // find the computers that are common to the set of computers and the set of connected computers
      std::set<std::string> intersection;
      std::set_intersection( aComputers.begin(), aComputers.end(),
                             aConnections[*computer_itr].begin(), aConnections[*computer_itr].end(),
                             std::inserter( intersection, intersection.begin() ) );
      // expand the set by using the set of common computers as the input set
      std::set<std::string> expandedNetwork = getLargestNetwork( intersection, aConnections, aCurrentNetwork );
      if ( expandedNetwork.size() > largestSet.size() )
      {
         largestSet = expandedNetwork;
      }
      aCurrentNetwork.erase( *computer_itr ); // remove the computer for the next loop
      // remove the computer from the set of computers to prevent searching for the same set again, update the iterator
      computer_itr = aComputers.erase( computer_itr );
   }
   return largestSet;
}

/**
 * @brief For part 1, count the number of sub networks of three interconnected computer within the complete network.
 *        For part 2, print computers names of the largest sub network of interconnected computers.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 */
void compute( const std::string aInputFilePath, const bool aPart1 )
{
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::map<std::string, std::set<std::string> > connections;
      std::set<std::string> computers;
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         computers.insert( line.substr( 0, 2 ) );
         computers.insert( line.substr( 3, 2 ) );
         connections[line.substr( 0, 2 )].insert( line.substr( 3, 2 ) );
         connections[line.substr( 3, 2 )].insert( line.substr( 0, 2 ) );
      }
      if ( aPart1 )
      {
         printf( "%d\n", getThreeComputerNetworksCount( connections ) );
      }
      else
      {
         std::set<std::string> currentSet;
         std::set<std::string> largestSet               = getLargestNetwork( computers, connections, currentSet );
         std::set<std::string>::iterator largestSet_itr = largestSet.begin();
         for (; largestSet_itr != largestSet.end(); largestSet_itr++ )
         {
            printf( "%s,", largestSet_itr->c_str() );
         }
         printf( "\n" );
      }
      inputFile.close();
   }
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
      printf( "Part 1 solution: " );
      compute( argv[1], true );
      printf( "Part 2 solution: " );
      compute( argv[1], false );
   }
   return 0;
}
