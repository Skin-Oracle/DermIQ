import { Button, StyleSheet, Text, View } from 'react-native';
import CameraPage from './pages/cameraPage';

export default function App() {
  return (
    <View style={styles.container}>
      <View>
        <CameraPage/>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
