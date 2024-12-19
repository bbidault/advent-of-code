// https://adventofcode.com/2024/day/9

#include <algorithm>
#include <fstream>
#include <vector>

/**
 * @brief Defragmentize the memory by moving individual memory cells from the back of the memory to the
 *        front most free cell.
 *
 * @param aInputFilePath the input file
 * @return the checksum of the resulting memory
 */
int64_t computePart1( const std::string aInputFilePath )
{
   int64_t checksum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         // initialize the memory
         std::vector<int> memory;
         int id = 0;
         for ( int i = 0; i < line.size(); i++ )
         {
            if ( i % 2 == 0 )
            {
               for ( int j = 0; j < ( line[i] - '0' ); j++ )
               {
                  memory.push_back( id );
               }
               id++;
            }
            else
            {
               for ( int j = 0; j < ( line[i] - '0' ); j++ )
               {
                  memory.push_back( -1 );
               }
            }
         }

         // defragmentize the memory
         std::vector<int> newMemory;
         int forwardItr  = 0;
         int backwardItr = memory.size() - 1;
         while ( forwardItr <= backwardItr )
         {
            if ( memory[forwardItr] != -1 )
            {
               newMemory.push_back( memory[forwardItr] );
               forwardItr++;
            }
            else if ( memory[backwardItr] != -1 )
            {
               newMemory.push_back( memory[backwardItr] );
               backwardItr--;
               forwardItr++;
            }
            else
            {
               backwardItr--;
            }
         }

         //checksum the memory
         for ( int i = 0; i < newMemory.size(); i++ )
         {
            checksum += i * newMemory[i];
         }
      }
      inputFile.close();
   }
   return checksum;
}

/**
 * @brief A block of memory, with an id if occupied by a file, -1 if free space
 */
struct MemoryBlock
{
   int  mSize          = 0;
   int  mId            = 0;
   bool mAttemptToMove = false;

   /**
    * @brief MemoryBlock constructor
    *
    * @param aSise the size of the block of memory
    * @param aId the identifier of the block of mem0ry, -1 if free space
    */
   MemoryBlock( const int aSize, const int aId )
   {
      mSize = aSize;
      mId   = aId;
   }
};

/**
 * @brief Defragmentize the memory by moving full blocks of occupied memory (files) from the back of the memory
 *        to the front most available block of free space that can fit the file. Attempt only once per file.
 *
 * @param aInputFilePath the input file
 * @return the checksum of the resulting memory
 */
int64_t computePart2( const std::string aInputFilePath )
{
   int64_t checksum = 0;
   std::ifstream inputFile( aInputFilePath );
   if ( inputFile.is_open() )
   {
      std::string line = "";
      while ( std::getline( inputFile, line ) )
      {
         // initialize the memory
         std::vector<MemoryBlock> memory;
         int id = 0;
         for ( int i = 0; i < line.size(); i++ )
         {
            if ( i % 2 == 0 )
            {
               memory.push_back( MemoryBlock( line[i] - '0', id ) );
               id++;
            }
            else
            {
               memory.push_back( MemoryBlock( line[i] - '0', -1 ) );
            }
         }

         // defragmentize the memory
         while ( std::any_of( memory.begin(),
                              memory.end(),
                              []( MemoryBlock block )
                              {
                                 // keep defragmentazing until we have moved or attempted to move all files
                                 return ( block.mId != -1 ) && ( false == block.mAttemptToMove );
                              } ) )
         {
            std::vector<MemoryBlock> newMemory;

            // identify the next file to move
            MemoryBlock fileToMove( 0, 0 );
            for ( int i = memory.size() - 1; i > 0; i-- )
            {
               if ( ( memory[i].mId != -1 ) && ( false == memory[i].mAttemptToMove ) )
               {
                  fileToMove = memory[i];
                  break;
               }
            }

            bool movedFile = false;                   // whether we moved the file already or not
            for ( int i = 0; i < memory.size(); i++ ) // iterate through the memory blocks
            {
               // if we encounter a file or we already moved the file of interest, copy the rest of the memory as is
               if ( ( memory[i].mId != -1 ) || movedFile )
               {
                  newMemory.push_back( memory[i] );
                  if ( movedFile && ( newMemory.back().mId == fileToMove.mId ) )
                  {
                     // if we have moved the file, replace the block of memory with free space
                     newMemory.back().mId = -1;
                  }
                  else if ( newMemory.back().mId == fileToMove.mId )
                  {
                     // we have failed to move this file toward the front of the memory
                     movedFile = true; // set the boolean to true to force the rest of the memory to copy has is
                     newMemory.back().mAttemptToMove = true;
                  }
                  else
                  {
                     // do nothing
                  }
               }
               else // if we encounter free space and we have not moved the file of interest yet, check if we can fit it
               {
                  int spaceLeft = memory[i].mSize - fileToMove.mSize; // the leftover free space after moving the file
                  if ( spaceLeft >= 0 )
                  {
                     newMemory.push_back( fileToMove );
                     if ( spaceLeft > 0 )
                     {
                        // if there is free space left, add it now
                        newMemory.push_back( MemoryBlock( spaceLeft, -1 ) );
                     }
                     movedFile = true;
                  }
                  else
                  {
                     newMemory.push_back( memory[i] ); // copy the block of free space as is
                  }
               }
            }
            memory = newMemory;
         }

         //checksum the memory
         int multiplier = 0;
         for ( int i = 0; i < memory.size(); i++ )
         {
            for ( int j = 0; j < memory[i].mSize; j++ )
            {
               if ( memory[i].mId != -1 )
               {
                  checksum += multiplier * memory[i].mId;
               }
               multiplier++;
            }
         }
      }
      inputFile.close();
   }
   return checksum;
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
      printf( "Part 1 solution: %ld\n", computePart1( argv[1] ) );
      printf( "Part 2 solution: %ld\n", computePart2( argv[1] ) );
   }
   return 0;
}
