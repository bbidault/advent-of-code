// https://adventofcode.com/2024/day/25

#include <fstream>
#include <vector>

/**
 * @brief Check whether a given key fits within a given lock.
 *
 * @param aKey a key
 * @param aLock a lock
 * @return bool whether a given key fits within a given lock
 */
bool valid( const std::vector<int> &aKey, const std::vector<int> aLock )
{
   for ( int i = 0; i < aKey.size(); i++ )
   {
      if ( aKey[i] + aLock[i] > 7 )
      {
         return false;
      }
   }
   return true;
}

/**
 * @brief Count the number of given keys that fit within given locks.
 *
 * @param aInputFilePath the input file
 * @return int the number of given keys that fit within given locks
 */
int compute( const std::string aInputFilePath )
{
   int count = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::vector<std::vector<int> > locks;
      std::vector<std::vector<int> > keys;
      // parse the input
      std::string line = "";
      bool readKey     = false;
      bool readNew     = true;
      while ( std::getline( inputFile, line ) )
      {
         if ( line.empty() )
         {
            readNew = true;
         }
         else if ( readNew )
         {
            if ( line == "#####" )
            {
               readKey = false;
               readNew = false;
               locks.push_back( { 1, 1, 1, 1, 1 } );
            }
            else
            {
               readKey = true;
               readNew = false;
               keys.push_back( { 0, 0, 0, 0, 0 } );
            }
         }
         else if ( readKey )
         {
            for ( int i = 0; i < line.size(); i++ )
            {
               if ( line[i] == '#' )
               {
                  keys.back()[i]++;
               }
            }
         }
         else // read lock
         {
            for ( int i = 0; i < line.size(); i++ )
            {
               if ( line[i] == '#' )
               {
                  locks.back()[i]++;
               }
            }
         }
      }
      // count the number of valid key/lock combinations
      for ( int i = 0; i < keys.size(); i++ )
      {
         for ( int j = 0; j < locks.size(); j++ )
         {
            if ( valid( keys[i], locks[j] ) )
            {
               count++;
            }
         }
      }
      inputFile.close();
   }
   return count;
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
      printf( "Part 1 solution: %d\n", compute( argv[1] ) );
   }
   return 0;
}
