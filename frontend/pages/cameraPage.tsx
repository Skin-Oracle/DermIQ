import { Button, StyleSheet, Text, View, Image, ScrollView } from 'react-native';
import * as FileSystem from 'expo-file-system';
import * as ImagePicker from 'expo-image-picker';
import tw from 'twrnc'
import React, {useState,useEffect } from 'react';
import axios from 'axios';

export default function cameraPage() {
  useEffect(() => {
    loadImages();
  }, []);

  const loadImages = async () => {
    await ensureDirExists();
    const files = await FileSystem.readDirectoryAsync(imgDir);
    if (files.length > 0) {
      setImages(files.map(f => imgDir + f));
    }
  };
  const imgDir = FileSystem.documentDirectory + 'images/';

  const ensureDirExists = async () => {
      const dirInfo = await FileSystem.getInfoAsync(imgDir);
      if (!dirInfo.exists) {
        await FileSystem.makeDirectoryAsync(imgDir, { intermediates: true });
      }
    };

  const selectImage = async (useLibrary: boolean) => {
      let result;
      const options: ImagePicker.ImagePickerOptions = {
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [3, 3],
        quality: 1,
      };
      if (useLibrary) {
        result = await ImagePicker.launchImageLibraryAsync(options);
      } else {
        const { status: cameraStatus } = await ImagePicker.requestCameraPermissionsAsync();
        if (cameraStatus !== 'granted') {
          alert('Sorry, we need camera permissions to make this work!');
          return;
        }
        result = await ImagePicker.launchCameraAsync(options);
      }
      if (!result.canceled) {
        saveImage(result.assets[0].uri);
      }
  };

  const saveImage = async (uri: string) => {
      await ensureDirExists();
      const filename = new Date().getTime() + '.jpg';
      const dest = imgDir + filename;
      await FileSystem.copyAsync({
        from: uri,
        to: dest,
      });
      setImages([...images, dest]);
      uploadImageToBackend(dest);
    };
    const uploadImageToBackend = async (imagePath: string) => {
      const formData = new FormData();
      const file = {
        uri: imagePath,
        type: 'image/jpeg', // or 'image/png', depending on your image type
        name: imagePath.split('/').pop() // Extracts the filename
      };
    
      // Cast the file object to 'any' to bypass TypeScript's type checking
      formData.append('uploaded_file', file as any);
    
      axios.post('http://127.0.0.1:8000/predict', formData, {
        headers: {
          // The content-type should be multipart/form-data
          'Content-Type': 'multipart/form-data'
        }
      })
      .then((response) => {
        console.log('Response from backend:', response.data);
      })
      .catch((error) => {
        console.error('Error uploading image:', error);
      });
    };
    
  const [images, setImages] = useState<string[]>([]);
  return (
    <View style={{flex:1, gap:20}}>
        <View style={tw `items-center mt-55`}>
            <Image style={tw `w-75 h-75`} resizeMode="contain" source={require('../components/images/DermLogo.png')}/>
        </View>
        <View style={{flexDirection:'row', justifyContent:'space-evenly', marginVertical: 10, marginTop:90}}>
            <Button title="Photo Library" onPress={()=> selectImage(true)} />
            <Button title="Capture Image" onPress={()=> selectImage(false)} />
        </View>
    </View>
  )
}

