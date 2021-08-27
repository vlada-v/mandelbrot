pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";


/**
 * @title AlmondBread
 * Creature - a contract for my non-fungible fractals.
 */
contract AlmondBread is Ownable, ERC721Enumerable {
  using Strings for uint256;

  struct Fractal {
    uint256 dna;
  }

  mapping(uint256 => Fractal) Fractals;
  
  // Max genesis Fractal available
  uint256 immutable public genesisFractalSupply;
  
  bool public saleIsActive = false;
  
  uint256 public constant MAX_MINTS_PER_TXN = 15;
  
  uint256 immutable public mintPrice;

  constructor(
    uint256 _genesisFractalSupply,
    uint256 _mintPrice
  ) ERC721("AlmondBread", "ABF")
  {
    genesisFractalSupply = _genesisFractalSupply;
    mintPrice = _mintPrice;
  }

  string private _baseTokenURI;

  // TODO: check if we can do something better
  function getRandomNumber(uint256 seed) internal view returns (uint256) {
    return uint256(keccak256(abi.encode(blockhash(block.number - 1), msg.sender, seed)));
  }

  // TODO: override the normal URI function to also return the DNA
  function _baseURI() internal view override returns (string memory) {
    return _baseTokenURI;
  }

  function setBaseTokenURI(string memory baseTokenURI) public onlyOwner {
    _baseTokenURI = baseTokenURI;
  }

  function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
    require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");

    string memory baseURI = _baseURI();
    return bytes(baseURI).length > 0 ? string(abi.encodePacked(baseURI, tokenId.toString(), "/", Fractals[tokenId].dna.toString())) : "";
  }

  function withdrawAll() public payable onlyOwner {
    payable(msg.sender).transfer(address(this).balance);
  }

  /*
  * Mint Fractal NFTs!
  */
  function mintFractals(uint256 numberOfTokens) public payable {
    require(saleIsActive, "Sale must be active to mint Fractal");
    require(numberOfTokens <= MAX_MINTS_PER_TXN, "Number of Fractal exceeds the max mint allowed per transaction");
    require(totalSupply() + numberOfTokens <= genesisFractalSupply, "Purchase would exceed max available Fractal");
    require(mintPrice * numberOfTokens <= msg.value, "Ether value sent is not correct");

    for(uint256 i = 0; i < numberOfTokens; i++) {
      uint256 mintIndex = totalSupply() + 1;
      _mintFractalGenesis(msg.sender, mintIndex);
    }
  }

  /*
  * Mint reserved Fractal NFTs for giveaways, devs, etc.
  */
  function reserveMint(uint256 numberOfTokens, address owner) public onlyOwner {
    require(totalSupply() + numberOfTokens <= genesisFractalSupply, "Purchase would exceed max available Fractals");
    for (uint256 i = 1; i <= numberOfTokens; i++) {
      uint256 mintIndex = totalSupply() + 1;
      _mintFractalGenesis(owner, mintIndex);
    }
  }


  function _mintFractalGenesis(address _owner, uint256 _index) private {
    uint256 randomNumber = getRandomNumber(_index);
    _mintFractal(_owner, _index, randomNumber);
  }


  function _mintFractal(address _owner, uint256 _index, uint256 _dna) private {
    _safeMint(_owner, _index);
    Fractals[_index] = Fractal(_dna);
  }

  /*
  * Pause sale if active, make active if paused.
  */
  function flipSaleState() public onlyOwner {
      saleIsActive = !saleIsActive;
  }
}