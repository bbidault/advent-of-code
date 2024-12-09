// https://adventofcode.com/2024/day/8

#include <fstream>
#include <map>
#include <set>
#include <sstream>
#include <vector>

/**
 * @brief Find the antinodes of a pair of given antennas within the given range.
 *
 * @param aAntenna an antenna location
 * @param aOtherAntenna an other antenna location
 * @param aAntinodesLoc the antinodes locations
 * @param aRangeMax the maximum x and y range of the map
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 */
void findAntinodes( const std::pair<int, int>      &aAntenna,
                    const std::pair<int, int>      &aOtherAntenna,
                    std::set<std::pair<int, int> > &aAntinodesLoc,
                    const std::pair<int, int>      &aRangeMax,
                    bool                           aPart1 )
{
   if ( false == aPart1 ) // for part 2, the antennas are antinodes too
   {
      aAntinodesLoc.insert( aAntenna );
      aAntinodesLoc.insert( aOtherAntenna );
   }
   // the distance from one antenna to the other
   int xDist = aOtherAntenna.first - aAntenna.first;
   int yDist = aOtherAntenna.second - aAntenna.second;
   int k     = 1; // multiplier for part 2 "harmonic frequencies"
   while ( true )
   {
      std::pair<int, int> aAntinodeCandidate = std::make_pair( aOtherAntenna.first + k * xDist,
                                                               aOtherAntenna.second + k * yDist );
      // if the antinode falls within the map
      if ( ( aAntinodeCandidate.first >= 0 ) &&
           ( aAntinodeCandidate.first < aRangeMax.first ) &&
           ( aAntinodeCandidate.second >= 0 ) &&
           ( aAntinodeCandidate.second < aRangeMax.second ) )
      {
         aAntinodesLoc.insert( aAntinodeCandidate );
         if ( aPart1 )
         {
            break; // stop with a single antinode for part 1
         }
      }
      else
      {
         break;
      }
      k++;
   }
}

/**
 * @brief Find the antinodes of a given set of antennas within the given map.
 *
 * @param aInputFilePath the input file
 * @param aPart1 whether we are solving part 1 (true) or part 2 (false)
 * @return the number of antinodes within the given map
 */
int compute( const std::string aInputFilePath, const bool aPart1 )
{
   // the antinodes locations, use a set to prevent duplicates
   std::set<std::pair<int, int> > antinodesLoc;

   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      // define a hashmap that sorts antennas by frequencies
      std::map<char, std::vector<std::pair<int, int> > > frequencies;

      std::string line = "";
      int xCoor        = 0;
      int yCoor        = 0;
      while ( std::getline( inputFile, line ) )
      {
         yCoor = 0;
         std::stringstream ss( line );
         char frequency;
         while ( ss >> frequency )
         {
            if ( frequency != '.' )
            {
               frequencies[frequency].push_back( std::make_pair( xCoor, yCoor ) );
            }
            yCoor++;
         }
         xCoor++;
      }

      // iterate through the frequencies
      std::map<char, std::vector<std::pair<int, int> > >::iterator m_itr = frequencies.begin();
      for (; m_itr != frequencies.end(); m_itr++ )
      {
         // iterate through pairs of antennas
         for ( int i = 0; i < m_itr->second.size(); i++ )
         {
            for ( int j = 0; j < m_itr->second.size(); j++ )
            {
               if ( i != j ) // don't compare an antenna with itself
               {
                  findAntinodes( m_itr->second[i],
                                 m_itr->second[j],
                                 antinodesLoc,
                                 std::make_pair( xCoor, yCoor ),
                                 aPart1 );
               }
            }
         }
      }
      inputFile.close();
   }
   return antinodesLoc.size();
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
